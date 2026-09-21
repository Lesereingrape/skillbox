#!/usr/bin/env bash
# Install skills from this repo into ~/.qoder/skills/.
# Usage: bash install.sh [skill-name ...]   (default: all)
set -euo pipefail
cd "$(dirname "$0")"
DEST="${HOME}/.qoder/skills"
mkdir -p "$DEST"

names=("$@")
if [ ${#names[@]} -eq 0 ]; then
  mapfile -t names < <(find skills -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort)
fi

for n in "${names[@]}"; do
  src="skills/$n"
  [ -f "$src/SKILL.md" ] || { echo "SKIP $n (no SKILL.md)"; continue; }
  rm -rf "$DEST/$n"
  cp -r "$src" "$DEST/$n"
  echo "INSTALLED $n -> $DEST/$n"
done
echo "Done. Restart the session or run /skills reload."
