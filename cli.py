#!/usr/bin/env python3
"""CLI entry point for the AI Internship Agent."""

import argparse
import sys
from pathlib import Path

# allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent))

from agent.loop import run_agent


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Find and rank internship listings (demo mode works offline)."
    )
    parser.add_argument(
        "-k",
        "--keywords",
        nargs="+",
        default=["machine learning", "internship"],
        help="Search keywords (default: machine learning internship)",
    )
    parser.add_argument(
        "-l",
        "--location",
        default="",
        help="Location filter (substring match)",
    )
    parser.add_argument(
        "--no-remote",
        action="store_true",
        help="Do not prefer remote roles",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=8,
        help="Max results in shortlist",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Use built-in demo listings (no network)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Write markdown shortlist to this file",
    )

    args = parser.parse_args(argv)

    md = run_agent(
        keywords=args.keywords,
        location=args.location,
        remote_ok=not args.no_remote,
        limit=args.limit,
        demo=args.demo,
    )

    print(md)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"\n[saved] {args.output}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
