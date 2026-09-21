#!/usr/bin/env python3
"""Render applications.json into a self-contained index.html dashboard.

Usage:
  python render_board.py <applications.json> [--template <path>] [--out index.html]

Prints one summary line on success. Exit 0 on success, 1 on any error.
"""
import argparse
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PLACEHOLDER = "__BOARD_DATA__"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("data")
    p.add_argument("--template", default=None, help="defaults to ../assets/dashboard-template.html")
    p.add_argument("--out", default=None, help="defaults next to the json file as index.html")
    args = p.parse_args()

    template_path = Path(args.template) if args.template else \
        Path(__file__).resolve().parent.parent / "assets" / "dashboard-template.html"
    data_path = Path(args.data)
    out_path = Path(args.out) if args.out else data_path.parent / "index.html"

    try:
        raw = json.loads(data_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"ERROR: cannot read {data_path}: {e}", file=sys.stderr)
        return 1
    if not isinstance(raw.get("applications"), list):
        print("ERROR: json must contain an 'applications' array (see references/schema.md)", file=sys.stderr)
        return 1

    try:
        template = template_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"ERROR: cannot read template {template_path}: {e}", file=sys.stderr)
        return 1
    if PLACEHOLDER not in template:
        print(f"ERROR: template missing {PLACEHOLDER}", file=sys.stderr)
        return 1

    # </script> 防护：避免 JSON 字符串提前闭合脚本标签
    payload = json.dumps(raw, ensure_ascii=False).replace("</", "<\\/")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(template.replace(PLACEHOLDER, payload), encoding="utf-8")

    n = len(raw["applications"])
    active = sum(1 for a in raw["applications"]
                 if a.get("status") in ("applied", "assessment", "interviewing", "offer"))
    print(f"OK: {out_path} rendered - {n} applications, {active} active, season={raw.get('season', '?')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
