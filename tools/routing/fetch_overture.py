"""Step 1: download the Minneapolis slice of Overture Maps (road segments, address points, places).

Overture Maps publishes OpenStreetMap roads and open address data as GeoParquet files on a public
bucket. This script reads only the row groups whose bounding box overlaps the area in settings.json,
using plain HTTPS range requests, so it needs no AWS tools.

    python tools/routing/fetch_overture.py            # writes tools/routing/cache/*.parquet

Output (not committed; about 50 MB): segments.parquet, addresses.parquet, places.parquet.
Data licenses: roads ODbL (OpenStreetMap contributors); addresses from the open sources listed in
each row's `sources`; places CDLA-Permissive-2.0.
"""
import concurrent.futures
import io
import json
import re
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import requests

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
BUCKET = "https://overturemaps-us-west-2.s3.us-west-2.amazonaws.com"
THEMES = {
    "segments": ("theme=transportation/type=segment",
                 ["id", "names", "subtype", "class", "connectors", "speed_limits", "access_restrictions",
                  "road_flags", "geometry", "bbox"]),
    "addresses": ("theme=addresses/type=address", ["id", "street", "number", "postcode", "postal_city", "geometry", "bbox"]),
    "places": ("theme=places/type=place", ["id", "names", "basic_category", "addresses", "geometry", "bbox", "confidence"]),
}
session = requests.Session()


class RangeFile(io.RawIOBase):
    """A read-only file object over HTTPS range requests, enough for pyarrow to read a Parquet footer
    and selected row groups."""

    def __init__(self, url):
        self.url, self.pos = url, 0
        self.size = int(session.head(url, timeout=60).headers["Content-Length"])

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=0):
        self.pos = offset if whence == 0 else (self.pos + offset if whence == 1 else self.size + offset)
        return self.pos

    def readinto(self, buffer):
        if self.pos >= self.size or not len(buffer):
            return 0
        end = min(self.size, self.pos + len(buffer)) - 1
        for attempt in range(5):
            try:
                r = session.get(self.url, headers={"Range": f"bytes={self.pos}-{end}"}, timeout=120)
                r.raise_for_status()
                break
            except requests.RequestException:
                if attempt == 4:
                    raise
        data = r.content
        buffer[:len(data)] = data
        self.pos += len(data)
        return len(data)


def list_files(prefix):
    keys, token = [], None
    while True:
        url = f"{BUCKET}/?list-type=2&prefix={prefix}" + (f"&continuation-token={requests.utils.quote(token)}" if token else "")
        listing = session.get(url, timeout=60).text
        keys += re.findall(r"<Key>([^<]*\.parquet)</Key>", listing)
        token = re.search(r"<NextContinuationToken>([^<]*)</NextContinuationToken>", listing)
        if not token:
            return keys
        token = token.group(1)


def _row_group_bbox(metadata, i):
    stats = {}
    group = metadata.row_group(i)
    for j in range(group.num_columns):
        column = group.column(j)
        if column.path_in_schema.startswith("bbox.") and column.statistics is not None and column.statistics.has_min_max:
            stats[column.path_in_schema] = (column.statistics.min, column.statistics.max)
    return stats


def read_bbox(key, box, columns):
    """Rows of one Parquet file whose bbox overlaps box = (xmin, ymin, xmax, ymax)."""
    xmin, ymin, xmax, ymax = box
    f = pq.ParquetFile(io.BufferedReader(RangeFile(f"{BUCKET}/{key}"), buffer_size=1 << 20))
    tables = []
    for i in range(f.metadata.num_row_groups):
        s = _row_group_bbox(f.metadata, i)
        if len(s) < 4 or s["bbox.xmin"][0] > xmax or s["bbox.xmax"][1] < xmin or s["bbox.ymin"][0] > ymax or s["bbox.ymax"][1] < ymin:
            continue
        t = f.read_row_group(i, columns=columns)
        bb = t.column("bbox").combine_chunks()
        inside = pc.and_(pc.and_(pc.less_equal(bb.field("xmin"), xmax), pc.greater_equal(bb.field("xmax"), xmin)),
                         pc.and_(pc.less_equal(bb.field("ymin"), ymax), pc.greater_equal(bb.field("ymax"), ymin)))
        t = t.filter(inside)
        if t.num_rows:
            tables.append(t)
    return tables


def main():
    settings = json.loads((HERE / "settings.json").read_text())
    b = settings["bbox"]
    box = (b["xmin"], b["ymin"], b["xmax"], b["ymax"])
    CACHE.mkdir(exist_ok=True)
    for name, (theme, columns) in THEMES.items():
        keys = list_files(f"release/{settings['overture_release']}/{theme}/")
        tables = []
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            for found in pool.map(lambda k: read_bbox(k, box, columns), keys):
                tables += found
        table = pa.concat_tables(tables, promote_options="permissive")
        pq.write_table(table, CACHE / f"{name}.parquet")
        print(f"{name}: {table.num_rows:,} rows from {len(keys)} files")


if __name__ == "__main__":
    main()
