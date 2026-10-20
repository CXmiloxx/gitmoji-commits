# Changelog

All notable changes to gitmoji-commits are documented here.

## [1.3.0] — 2026-10-20

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

## [1.2.0] — 2026-10-13

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

## [1.1.0] — 2026-09-15

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

## [1.0.0] — 2026-09-15

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
