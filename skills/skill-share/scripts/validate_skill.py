#!/usr/bin/env python3
"""Validate a skill directory against the Qoder skill spec.

Usage:
  python validate_skill.py <skill-dir> [<skill-dir> ...]

Prints one PASS/FAIL line per skill plus the skill name; failures list reasons.
Exit 0 only when every skill passes.
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NAME_RE = re.compile(r"^[a-z0-9-]+$")


def validate(skill_dir: Path) -> list[str]:
    errs = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return ["SKILL.md missing"]
    text = md.read_text(encoding="utf-8", errors="replace")

    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["frontmatter must start with --- and end with ---"]
    fm = m.group(1)
    body = text[m.end():]

    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc = re.search(r"^description:\s*(.+)$", fm, re.M)
    if not name:
        errs.append("frontmatter missing name")
    elif not NAME_RE.match(name.group(1).strip()):
        errs.append(f"name not hyphen-case: {name.group(1).strip()}")
    elif name.group(1).strip() != skill_dir.name:
        errs.append(f"folder '{skill_dir.name}' != name '{name.group(1).strip()}'")
    if not desc:
        errs.append("frontmatter missing description")
    elif len(desc.group(1).strip()) > 1024:
        errs.append(f"description too long ({len(desc.group(1).strip())} > 1024)")
    elif "\n" in desc.group(1):
        errs.append("description must be a single line")

    if body.count("\n") > 500:
        errs.append(f"body too long ({body.count(chr(10))} lines > 500)")
    if "TODO:" in text:
        errs.append("unresolved TODO: found")
    for extraneous in ("README.md", "CHANGELOG.md", "INSTALL.md"):
        if (skill_dir / extraneous).exists():
            errs.append(f"extraneous {extraneous} in skill dir")
    for sub in ("scripts", "references", "assets"):
        d = skill_dir / sub
        if d.is_dir() and not any(d.iterdir()):
            errs.append(f"empty dir {sub}/")
    return errs


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_skill.py <skill-dir> [...]", file=sys.stderr)
        return 2
    ok = True
    for arg in sys.argv[1:]:
        errs = validate(Path(arg))
        name = Path(arg).name
        if errs:
            ok = False
            print(f"FAIL {name}: " + "; ".join(errs))
        else:
            print(f"PASS {name}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
