"""Command line: python -m mps_model <command> [options]

  run          run the model and write every table and figure to results/
  figures      redraw the figures from the tables already in results/
  verify       compare results/ with reference_outputs/
  assumptions  regenerate docs/assumptions.md from config/assumptions.json
"""
import argparse
import sys
import time

from . import paths


def _run(args):
    from .pipeline import run
    started = time.time()
    run(args.results, reuse_curve=args.reuse_search, max_n=args.max_n, unconstrained=not args.skip_unconstrained,
        figures=not args.skip_figures, deck_images=args.deck_images, assumptions_path=args.assumptions)
    print(f"Finished in {time.time() - started:.0f} s")


def _figures(args):
    from .assumptions import Assumptions
    from .figures import draw_all
    draw_all(paths.ResultsDir(args.results), Assumptions.load(args.assumptions or paths.ASSUMPTIONS_FILE),
             deck_images=args.deck_images)


def _verify(args):
    from .verify import verify
    print(f"Comparing {args.results} with {args.reference}")
    ok = verify(args.results, args.reference)
    print("All tables match." if ok else "Some tables differ.")
    return 0 if ok else 1


def _assumptions(args):
    from .assumptions_doc import write_assumptions_doc
    path = write_assumptions_doc()
    print(f"Wrote {path}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m mps_model", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="run the model and write tables and figures")
    run.add_argument("--results", default=paths.DEFAULT_RESULTS_DIR, help="output folder (default: results/)")
    run.add_argument("--assumptions", default=None, help="assumptions file (default: config/assumptions.json)")
    run.add_argument("--reuse-search", metavar="CSV", default=None,
                     help="skip the search and re-evaluate the closure sets in a saved net_savings_by_closures.csv")
    run.add_argument("--max-n", type=int, default=None, help="largest number of closures to search (default: 30)")
    run.add_argument("--skip-unconstrained", action="store_true",
                     help="skip the second search without growth protection (dashed line in figure 1)")
    run.add_argument("--skip-figures", action="store_true", help="write tables only")
    run.add_argument("--deck-images", action="store_true", help="also write images sized for our slide deck")
    run.set_defaults(func=_run)

    figures = sub.add_parser("figures", help="redraw figures from existing result tables")
    figures.add_argument("--results", default=paths.DEFAULT_RESULTS_DIR)
    figures.add_argument("--assumptions", default=None)
    figures.add_argument("--deck-images", action="store_true")
    figures.set_defaults(func=_figures)

    verify = sub.add_parser("verify", help="compare a results folder with reference_outputs/")
    verify.add_argument("--results", default=paths.DEFAULT_RESULTS_DIR)
    verify.add_argument("--reference", default=paths.REFERENCE_OUTPUTS_DIR)
    verify.set_defaults(func=_verify)

    assumptions = sub.add_parser("assumptions", help="regenerate docs/assumptions.md")
    assumptions.set_defaults(func=_assumptions)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
