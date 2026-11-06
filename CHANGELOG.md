# Changelog

All notable changes to gitmoji-commits are documented here.

## [1.1.0] — 2026-11-06

### Added

- `checks/header.pattern`, `checks/forbidden.pattern` and `checks/review.pattern`: the agent validates every message with `git grep --no-index` before committing. The header check rejects malformed headers and every pair outside the allowlist; the forbidden check catches AI credit, leading verbs in five languages, body headings and WIP gitmojis; the review check flags long lines, "see X" pointers and session-only terms. Only git is needed, on every OS.
- Explicit rule precedence: user request, then repository rules, then the skill, then history (format only).
- "Rules that never bend": no `--no-verify`, no `--no-gpg-sign`, no push, no amend of pushed commits, no commit during a merge or rebase.
- A fixed plan format before several commits, a commit order (security fixes, bug fixes, refactors, feature, the rest) and a fixed final report.
- Body guidance for `refactor`, `perf`, `build` and `revert`, with examples.
- `references/special-cases.md`: failing or rewriting hooks, commitlint without a gitmoji parser, `.gitmojirc`, signed commits, DCO, detached HEAD, large files, submodules, "improve a message only".
- `tools/build_checks.py` and `tests/`: regenerate `header.pattern` from the catalog and fail when the catalog, the allowlist in `SKILL.md`, the pattern, the fixtures or the versions in `SKILL.md` and `.claude-plugin/plugin.json` disagree. CI runs it on every push.
- Claude Code plugin and marketplace manifests in `.claude-plugin/`: `/plugin install gitmoji-commits --marketplace CXmiloxx/gitmoji-commits`. They point at the same skill folder as `npx skills add`, so there is no copy to keep in sync.
- `allowed-tools` in the frontmatter, limited to the git commands the skill runs, so agents that support it ask for fewer permissions.
- `tools/link-local.sh`: links `~/.agents/skills/gitmoji-commits` and `~/.claude/skills/gitmoji-commits` to the checkout for local development.
- Staged-only mode: when the user staged something themselves, only that is committed and the unstaged rest is reported.
- Issue references taken from the branch name when history uses them.
- Diffs are read with `--no-ext-diff`, and lockfiles, minified bundles, snapshots and binaries are judged by `--stat` only.

### Changed

- The skill lives in `skills/gitmoji-commits/` (`SKILL.md`, `references/`, `checks/`). Only that folder is installed; tests, tools and READMEs stay in the repository.
- Gitmojis are written exactly as the catalog spells them, variation selector included (`⚡️`, not `⚡`), and `header.pattern` rejects the bare form, matching `commitlint-config-gitmoji`.
- `SKILL.md` keeps only what every commit needs. Type examples and ambiguous cases moved to `references/types.md`, message examples to `references/message.md`, hunk splitting to `references/splitting.md`. A table says when to read each file.
- Hunk splitting uses `git diff --output` and `git apply --cached --recount` instead of hand-built blobs and `git update-index --cacheinfo`. Commits built from part of a file are verified in a `git worktree` instead of `git archive | tar`.
- `SKILL.md` body is about a quarter shorter (18.4k to 14k characters), inside the Agent Skills size guideline, with the same rules.
- Pushing is allowed when the user asks for it; before, "never push" contradicted that request.
- Instruction files have explicit type rules: new agent capability is `feat`, corrected or adjusted behavior is `fix`, wording only is `docs`.

### Fixed

- gitmoji-cli configuration is read with its real keys (`emojiFormat`, `scopePrompt`, `capitalizeTitle`, and the `"gitmoji"` key in `package.json`) instead of `format` and `scopes`, which don't exist.
- `references/convention-template.md` is now referenced from the skill and no longer tells the agent to copy gitmojis seen in history, which contradicted "history never decides the pair".

## [1.0.0] — 2026-10-20

### Changed

- Body for `feat` and `fix` follows before → now → why it matters, written for a teammate outside the session, with a ❌/✅ example. Technical details (endpoint, limit, expiry) only with their reason.
- Body must be self-contained: no "see/ver X" pointers. A referenced file is named by its path from the repository root together with what it holds.
- Body uses the code's real names (identifiers in backticks) instead of terms invented during the session. Lines wrap at 72 characters. No section headings inside the body.
- `BREAKING CHANGE:` uses one footer per break, each with the real name and the action consumers must take, with a ❌/✅ example.
- Grouping is by intent, never by layer, and a large diff is split so security and bug fixes don't hide inside a `feat`.
- `feat` pairs fail fast, and the header is checked against its exact shape (`<gitmoji> <type>(<scope>)<!>: <title>`, spacing, case, 72 characters).
- Scope may be new for a new area, and is never a table name.
- Instruction files (`SKILL.md`, `AGENTS.md`…) moved out of the leftovers list, where they could be left unstaged.
- Title examples now carry their gitmoji; the dependency example is `⬆️ build(deps)` instead of `chore` with a leading verb.

### Documentation

- Both READMEs (English and Spanish) show a badge with the latest release and link to `CHANGELOG.md`.
- Grouping by intent, scope reuse and self-contained bodies are described in both READMEs.

## [0.3.0] — 2026-10-13

### Changed

- The gitmoji is chosen after the type and only from that type's allowlist, now embedded in `SKILL.md`. The catalog is no longer searched across sections, which let a commit pick 🗃️ for a `feat` because it touched the database.
- History decides only the emoji format (character or shortcode), never the pair. Invalid pairs in past commits (`🗃️ feat`, `📚 docs`) are reported, not copied. Only a written convention file can allow a pair outside the allowlist.
- Each catalog section now lists every gitmoji its type may use, including conditional ones borrowed from another type.
- Catalog descriptions no longer cover "new" things outside ✨ (🦺, 💫, 🛂, 🗃️, 🌐, ✈️, 📈, 💄): anything new is `✨ feat`.
- Step 6b covers repairs and intentional adjustments of existing behavior, as model A intended. When 6a and 6b both apply, `feat` wins.
- The header is validated twice: before writing the message and on the real commit with `git log -1`.
- Technical layers (`schema`, `db`, `api`, `ui`) are not scopes unless history already uses them consistently.

### Added

- Table of wrong pairs that look reasonable (`🗃️ feat`, `💄 feat`, `🦺 feat`, `📚 docs`…).
- Ambiguous cases for database restructuring and permissions.

## [0.2.0] — 2026-09-15

### Changed

- **BREAKING:** Type classification model reversed to Conventional Commits standard (Model A). Changes that intentionally alter behavior (business rules, UI restyling, API adaptation, new validations) now use `fix` with area gitmojis (👔 🎨 🚸 🛂 🦺 👽️) instead of `refactor`. This ensures they publish in changelog and semver via release tools (`semantic-release`, `release-please`).
- Consolidated duplicate rules across sections. Moved gitmoji selection guidance from section 5a to catalog. Removed quick-reference table, separate refactor-vs-style section, common mistakes section, and standalone final checklist (now integrated in section 8).
- Added instruction files (SKILL.md, AGENTS.md, CLAUDE.md) as non-documentation: their changes go through type decision (step 6), not automatic `docs`.
- Expanded step 2 to handle mixed changes in one file without `git add -p`: procedure for selective hunk extraction, verification, and staging via `git update-index`.
- Added verification step after commits assembled from intermediate file versions: extract, build/typecheck, verify final tree.
- Added guidance for breaking changes: concrete criteria (removed/renamed API, field type change, new required parameter, changed default behavior).
- Clarified scope naming: domain-driven, match history, lowercase only.

### Fixed

- Resolved 14 internal contradictions (Model B conflicts with Conventional Commits and semver tools; import reordering classification; metrics in examples vs rules; missing gitmojis in examples; verbs in titles marked as anti-pattern).
- Fixed 10 invalid examples that failed their own validation (wrong gitmojis, verbs in titles, prohibited metrics).
- Aligned `README.md` and `README.es.md` to Model A (moved definitions from Model A in README to Model B in SKILL; now consistent).

### Removed

- Quick-reference type table (duplicated step 4).
- Section 10 (Refactor vs style — integrated into step 8).
- Section 11 (Common mistakes — guidance moved into step 4 and rules).
- Standalone final checklist (section 12 — merged into section 8).
- Multi-language title examples table (examples now show intent, not just language).

## [0.1.0] — 2026-09-15

### Added

- Clarification of fix vs refactor with examples and ambiguous cases (database, APIs, validation, UI, perf, accessibility).
- Real-world commit examples (feat, fix, refactor, docs, perf).
- Specialized gitmoji guidance (when to use 👔 💄 🚸 🛂 🦺 👽️).
- Scope naming guide: domain-driven, consistency rules.
- Anti-patterns table for commit messages.
- Common mistakes by agents and developers.
- Final checklist before commit.

### Changed

- Expanded type decision with rules and ambiguous cases.
- Added real examples to message section.

## [Initial] — Before versioning

- Gitmoji Commits skill with core sections: read repository, exclude secrets, group commits, type decision, gitmoji selection, language detection, message format, commit procedure, special cases.
