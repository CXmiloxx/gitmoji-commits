# Type decision: details and ambiguous cases

Read this when the ten questions in SKILL.md step 4 do not give an obvious answer, or when the change touches a database, an external API, validation, permissions, UI or instruction files.

## The questions with examples

| # | Question | Yes → | Example yes | Example no |
|---|---|---|---|---|
| 1 | Does the group undo an earlier commit? | `revert` | `git revert` of a broken release | Removing a feature on purpose (→ step 6, often 💥) |
| 2 | Is **every** path documentation or a code comment? | `docs` | README, `docs/`, API reference, docblock | `SKILL.md`, `AGENTS.md`, `CLAUDE.md` (instruction files) |
| 3 | Is **every** path a test, mock, fixture or snapshot? | `test` | `test_*.py`, `__mocks__/`, snapshots | Production code with its tests |
| 4 | Is **every** path a CI/CD pipeline file? | `ci` | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` | A script the pipeline calls |
| 5 | Is **every** path build, packaging or dependency? | `build` | `package.json` + lockfile, `Dockerfile`, `pyproject.toml` | Test runner or linter config (→ `chore`) |
| 6a | Can someone now do something they could not do before? | `feat` | New endpoint, command, option, filter, validation rule, role | A rewritten screen that does the same thing |
| 6b | Does existing behavior change, repaired or adjusted on purpose? | `fix` | Wrong total now right; business rule changed; UI restyled | Same output, only faster (→ `perf`) |
| 6c | Observable change, but neither 6a nor 6b? | `chore` | Log output, release bump, seeds | — |
| 7 | Same behavior, measurably faster or lighter? | `perf` | Index, fewer round trips, smaller bundle | "Should be faster" with nothing measured (→ `refactor`) |
| 8 | Same behavior, formatting only? | `style` | Whitespace, import order, lint autofix | CSS or UI changes (→ step 6) |
| 9 | Same behavior, code restructured? | `refactor` | Extract, rename, move, simplify, dead code removed | — |
| 10 | Nothing matched? | `chore` | — | Never a catch-all for things you did not classify |

## Tie rules

1. Steps 2–5 need *every* path to qualify. One production or instruction file sends the group to step 6.
2. Step 6a is about capability, not size. A one-line option nobody had is `feat`; a rewritten screen doing the same is `refactor` or `style`.
3. The type comes from the diff only, before any emoji is considered. The area touched (database, UI, API) never decides the type.
4. When 6a and 6b are both true (a restructure that also opens a new capability), 6a wins: `feat`.
5. A breaking change keeps its type. The gitmoji becomes 💥, the header gets `!`, and the body gets one `BREAKING CHANGE:` footer per break.

## What counts as a breaking change

Consumers (users, clients, other services, deploy scripts) must change something:

- removed or renamed endpoint, route, field, flag, command, environment variable or public function
- changed field type, response shape or default behavior
- a parameter that was optional becomes required
- dropped support for a runtime, platform or API version
- renamed or dropped table or column that other code or services read

Internal renames nobody outside the module sees are not breaking.

## Instruction files

`SKILL.md`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, prompt templates and agent rules are the product of the repository that holds them: their "behavior" is what the agent does after reading them.

- The agent can now do something it could not → `✨ feat`
- The agent did something wrong and now does it right, or a rule was adjusted on purpose → `🐛 fix` (or the area gitmoji from the `fix` row that fits the whole commit)
- Wording only, the agent behaves the same → `docs` (`📝`, or `✏️` for a typo)
- Same behavior, restructured (sections moved, duplication removed) → `♻️ refactor`

## Ambiguous cases

Ask: *was this broken or missing and now works, or did we intentionally change working behavior?*

**Database.**
- New tables or columns that enable a capability → `✨ feat`, in the same commit as the code that uses them.
- Restructuring existing data that also opens a new possibility (one record shared by two roles that used to be duplicated) → `✨ feat`.
- Fixing corrupted data, a broken migration or a wrong constraint → `🗃️ fix`.
- Same result, only faster (index, query plan) → `🗃️ perf` or `⚡️ perf`.
- Renamed or dropped tables or columns that other code reads → add 💥 and `!`.

**External APIs.**
- The provider changed its format and we adapt → `👽️ fix`.
- The provider fixed its bug, we remove our workaround, result identical → `♻️ refactor`.

**Validation.**
- A rule that did not exist → `✨ feat`.
- An existing rule changed per policy → `🦺 fix`.
- Typo in a validation message → `💬 fix`.

**Permissions.**
- A new role or permission → `✨ feat`.
- An access rule changed → `🛂 fix`. A missing check closed → `🔒️ fix`.

**UI.**
- Broken on mobile or in dark mode, now works → `📱 fix` or `💄 fix`.
- Restyling, colors, layout → `💄 fix`. A new theme or screen → `✨ feat`.
- Fewer steps, clearer copy, better feedback → `🚸 fix`.

**Dependencies.**
- Upgrade alone → `⬆️ build(deps)`. Upgrade forced by a security advisory → still `⬆️ build`, and the body names the advisory.
- A dependency added only to implement a feature → inside that `✨ feat` commit, never alone.
- Code changes needed to survive an upgrade go with the upgrade: `⬆️ build` if behavior is identical, `fix` if behavior changed.

**Configuration.**
- Linter, formatter, editor, `tsconfig` → `🔧 chore`. Bundler, compiler, packaging → `🔧 build`.
- A config value that changes what users see (timeout, limit, feature default) → step 6, usually `fix`.

**Files.**
- Rename or move only → `🚚 refactor` (`🚚 chore` if only config, docs or asset paths moved).
- Removal of dead code → `⚰️ refactor`; of a public capability → 💥.
- Submodule pointer bump → `⬆️ build(deps)`.

## Wrong pairs that look reasonable

| ❌ | ✅ | Why |
|---|---|---|
| `🗃️ feat(empresas): …` | `✨ feat(empresas): …` | New capability: only ✨. The database is the area, not the intent |
| `💄 feat(ui): dark mode` | `✨ feat(ui): dark mode` | A new theme is a new capability |
| `🦺 feat(signup): password strength rule` | `✨ feat(signup): …` | A rule that did not exist is `feat` |
| `🌐 feat(checkout): pt-BR locale file` | `✨ feat(checkout): checkout available in Portuguese` | A new language is `feat` |
| `🐛 refactor(orders): …` | `♻️ refactor(orders): …` | 🐛 belongs to `fix` |
| `✨ fix(cart): …` | `🐛 fix(cart): …` | ✨ belongs to `feat` |
| `📚 docs(readme): …` | `📝 docs(readme): …` | 📚 is not a gitmoji |
| `🎨 fix(ui): new button colors` | `💄 fix(ui): …` | 🎨 is code formatting, never CSS or UI |
| `🗃️ fix(db): faster report query` | `🗃️ perf(reports): …` | Speed only, same result: `perf` |
| `🔧 chore: updated dependencies` | `⬆️ build(deps): React 18.2` | Dependencies are `build` |
