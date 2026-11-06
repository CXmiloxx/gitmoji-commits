#!/usr/bin/env sh
# Maintainer tool. Points the installed skill at this checkout, so every edit
# is live for Claude Code and any agent that reads ~/.agents/skills, with no
# copy to keep in sync. An existing non-link install is moved aside, not deleted.
set -eu
src="$(cd "$(dirname "$0")/.." && pwd)/skills/gitmoji-commits"
agents="$HOME/.agents/skills/gitmoji-commits"
claude="$HOME/.claude/skills/gitmoji-commits"
mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills"
for dest in "$agents" "$claude"; do
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    mv "$dest" "$dest.bak.$(date +%s)"
    echo "moved old install to $dest.bak.*"
  fi
done
ln -sfn "$src" "$agents"
ln -sfn "../../.agents/skills/gitmoji-commits" "$claude"
echo "linked: $claude -> $agents -> $src"
