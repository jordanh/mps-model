"""Writes docs/assumptions.md: every value in config/assumptions.json with its source, as tables."""
import json

from .paths import ASSUMPTIONS_FILE, REPO_ROOT

HEADER = """# Assumptions

Generated from `config/assumptions.json` by `python -m mps_model assumptions`. Do not edit by hand:
change the JSON file and regenerate.

**ESTIMATE** marks a value with no public figure behind it; it is a reasoned estimate and a good
candidate for sensitivity testing. **PLACEHOLDER** marks a value that has not been researched yet.
"""


def _cell(value):
    text = json.dumps(value) if isinstance(value, (dict, list)) else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _section_rows(entries, prefix=""):
    rows = []
    for key, entry in entries.items():
        if key.startswith("_"):
            continue
        if isinstance(entry, dict) and "value" in entry:
            rows.append((prefix + key, entry["value"], entry.get("src", "")))
        elif isinstance(entry, dict) and all(isinstance(v, dict) for k, v in entry.items() if not k.startswith("_")):
            rows += _section_rows(entry, prefix=f"{prefix}{key}.")
        else:
            rows.append((prefix + key, entry, ""))
    return rows


def _staff_floor_table(floors):
    lines = []
    for level, roles in floors.items():
        if level.startswith("_"):
            continue
        lines += [f"\n**{level.title()}**\n", "| Role | Minimum FTE | Students per FTE | Salary used |", "|---|---|---|---|"]
        for role, rule in roles.items():
            lines.append(f"| {role.replace('_', ' ')} | {rule['floor']} | {rule['per']:,} | {rule['cost']} |")
    return lines


def write_assumptions_doc(path=REPO_ROOT / "docs" / "assumptions.md"):
    raw = json.loads(ASSUMPTIONS_FILE.read_text())
    lines = [HEADER]
    for section, entries in raw.items():
        if section.startswith("_"):
            continue
        lines.append(f"\n## {section.replace('_', ' ').capitalize()}\n")
        doc = entries.get("_doc") if isinstance(entries, dict) else None
        if doc:
            lines.append(doc + "\n")
        if section == "staff_floors":
            lines += _staff_floor_table(entries)
            continue
        lines += ["| Key | Value | Source |", "|---|---|---|"]
        for key, value, src in _section_rows(entries):
            lines.append(f"| `{key}` | {_cell(value)} | {_cell(src)} |")
    path.write_text("\n".join(lines) + "\n")
    return path
