#!/usr/bin/env python3
"""Maintainer tool. Not needed to use the skill.

references/gitmojis.md is the single source of truth for which gitmoji each
type may carry. This script:

  build   regenerates checks/header.pattern from the catalog
  check   fails if SKILL.md's allowlist, the catalog and header.pattern
          disagree, if SKILL.md and .claude-plugin/plugin.json carry
          different versions, or if any fixture in tests/ is classified
          wrongly by the real `git grep` the skill runs

Usage: python3 tools/build_checks.py [build|check]
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "gitmoji-commits"
CATALOG = SKILL_DIR / "references" / "gitmojis.md"
SKILL = SKILL_DIR / "SKILL.md"
CHECKS = SKILL_DIR / "checks"
TESTS = ROOT / "tests"

TYPES = ["feat", "fix", "refactor", "perf", "style", "docs",
         "test", "build", "ci", "chore", "revert"]
VS16 = "️"
SCOPE = r"(\([a-z0-9][a-z0-9._/,-]*\))?"
TITLE = r": [^ ](.*[^. ])?$"


def bare(emoji):
    return emoji.replace(VS16, "")


def parse_catalog():
    """{type: [(emoji, shortcode), ...]} in catalog order."""
    sections, current = {}, None
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (\w+)\s*$", line)
        if m:
            current = m.group(1) if m.group(1) in TYPES else None
            if current:
                sections[current] = []
            continue
        if current:
            row = re.match(r"^\| (\S+) \| `(:[a-z0-9_+-]+:)` \|", line)
            if row:
                sections[current].append((row.group(1), row.group(2)))
    missing = [t for t in TYPES if not sections.get(t)]
    if missing:
        sys.exit(f"catalog: no rows for {missing}")
    return sections


def parse_skill_allowlist():
    """{type: set(bare emoji)} from the allowlist table in SKILL.md."""
    rows = {}
    for line in SKILL.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| `(\w+)` \| ([^|]*) \| ([^|]*) \|$", line)
        if m and m.group(1) in TYPES:
            cells = (m.group(2) + " " + m.group(3)).replace("—", " ")
            rows[m.group(1)] = {bare(e) for e in cells.split()}
    return rows


def alternatives(pairs):
    seen, out = set(), []
    for emoji, code in pairs:
        # Exact catalog spelling only: commitlint-config-gitmoji compares bytes,
        # so a gitmoji without its variation selector (⚡ for ⚡️) is rejected.
        for alt in (emoji, code):
            if alt and alt not in seen:
                seen.add(alt)
                out.append(alt)
    return out


def render_pattern(sections):
    lines = []
    for t in TYPES:
        alts = "|".join(alternatives(sections[t]))
        lines.append(f"^({alts}) {t}{SCOPE}{TITLE}")
    lines.append(f"^(💥|:boom:) ({'|'.join(TYPES)}){SCOPE}!{TITLE}")
    return "\n".join(lines) + "\n"


def git_grep_lines(pattern_file, target, flags=()):
    """Line numbers of `target` matched by the patterns, using git itself."""
    cmd = ["git", "grep", "--no-index", "-n", "-h", "-E", *flags,
           "-f", str(pattern_file), "--", target.name]
    res = subprocess.run(cmd, cwd=target.parent, capture_output=True,
                         text=True, encoding="utf-8")
    if res.returncode not in (0, 1):
        sys.exit(f"git grep failed: {res.stderr}")
    return {int(l.split(":", 1)[0]) for l in res.stdout.splitlines() if l}


def fixture_lines(path):
    """(line number, text) of non-empty, non-comment lines."""
    out = []
    for i, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if text.strip() and not text.startswith("#"):
            out.append((i, text))
    return out


def check_fixtures():
    errors = []
    plan = [
        ("header.pattern", "headers-valid.txt", (), True),
        ("header.pattern", "headers-invalid.txt", (), False),
        ("forbidden.pattern", "forbidden-hit.txt", ("-i",), True),
        ("forbidden.pattern", "headers-valid.txt", ("-i",), False),
        ("review.pattern", "review-hit.txt", ("-i",), True),
    ]
    for pattern, fixture, flags, should_match in plan:
        target = TESTS / fixture
        matched = git_grep_lines(CHECKS / pattern, target, flags)
        for n, text in fixture_lines(target):
            if (n in matched) != should_match:
                verb = "should match" if should_match else "should NOT match"
                errors.append(f"{pattern} {verb} {fixture}:{n}: {text}")
    return errors


def check_versions():
    """SKILL.md metadata and the plugin manifest must carry the same version."""
    import json
    skill = re.search(r'^  version: "([^"]+)"$', SKILL.read_text(encoding="utf-8"), re.M)
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if not skill:
        return ["SKILL.md: metadata.version missing"]
    if skill.group(1) != plugin.get("version"):
        return [f"version mismatch: SKILL.md {skill.group(1)} vs plugin.json {plugin.get('version')}"]
    return []


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "check"
    sections = parse_catalog()
    expected = render_pattern(sections)
    pattern_file = CHECKS / "header.pattern"

    if mode == "build":
        pattern_file.write_text(expected, encoding="utf-8")
        print(f"wrote {pattern_file.relative_to(ROOT)}")
        return

    errors = []
    if pattern_file.read_text(encoding="utf-8") != expected:
        errors.append("checks/header.pattern is stale: run `build`")

    skill = parse_skill_allowlist()
    for t in TYPES:
        cat = {bare(e) for e, _ in sections[t]}
        got = skill.get(t, set())
        if cat != got:
            errors.append(f"SKILL.md allowlist `{t}` differs from catalog: "
                          f"only in SKILL {sorted(got - cat)}, "
                          f"only in catalog {sorted(cat - got)}")

    errors += check_versions()
    errors += check_fixtures()
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("ok: catalog, SKILL.md allowlist, header.pattern and fixtures agree")


if __name__ == "__main__":
    main()
