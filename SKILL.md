---
name: gitmoji-commits
description: 'Writes git commits with gitmoji and Conventional Commits (`<gitmoji> type(scope): title`) that match the current repository. It reads recent history to detect the commit language (any language), the scopes and the emoji style. It groups changes into single-intent commits, picks the right type (feat, fix, refactor, perf, style, docs, test, build, ci, chore, revert) and a valid gitmoji out of all 75, and writes clear titles and bodies. It keeps secrets, exposed tokens and leftover session or temporary files out of commits. Programming terms stay in English and no AI attribution is added. Works with plain git on Linux, macOS and Windows. Use it whenever the user asks to commit, write or improve a commit message, split or group changes into commits, or prepare commits for a pull request, even if they only say "commit this", "haz el commit" or "fais le commit".'
license: MIT
metadata:
  author: CXmiloxx
  version: "1.1.0"
---

# Gitmoji Commits

One commit, one intent, written the way an experienced developer would write it:

```
🐛 fix(auth): sessions closed after a password change

Changing the password left other devices signed in, so a stolen session
kept working. Every active session now ends when the password changes.
```

Only `git` is needed. Every command below runs the same in bash, zsh, PowerShell and cmd.

## 1. Read the repository

Run once per session:

```
git status --short
git diff --stat
git diff --cached --stat
git log -n 20 --no-merges --format=%s
git ls-files "*COMMIT_CONVENTION*" "*commitlint*" ".gitmojirc*" "CONTRIBUTING*"
```

(`git log` fails on a repository with no commits. Treat that as a new project.)

From that output, settle four things without writing them down:

- **Existing rules.** If the last command lists files, read only their commit section. They override this skill, and commits must pass any commitlint or hook config.
- **Language.** See section 6.
- **Scopes.** Reuse the ones in history. For a new area, name the module or domain.
- **Emoji style.** Write the character (`✨`) unless history uses shortcodes (`:sparkles:`). If history consistently uses its own emoji for a type (for example `📚` for docs), keep it. If a type has a custom emoji in history, keep using that emoji.

Then read the changes themselves: `git diff`, `git diff --cached`, and any untracked files. For a large diff, read one path at a time with `git diff -- <path>`. For an untracked folder (`git status` shows `folder/`), list what's inside with `git status --short -uall -- <folder>`.

## 2. Leave out what must not be committed

Check every changed and untracked file before grouping. Nothing on this list gets staged unless the user explicitly confirms it.

**Secrets.** Search the changed files, using the paths `git status` listed:

```
git grep --untracked -n -I -i -E "(api_?key|secret|token|passw|pwd|credential|private_?key|access_?key|auth_?key)[A-Za-z0-9_-]*.{0,3}[:=].{0,3}[A-Za-z0-9/+_-]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_|sk-[A-Za-z0-9_-]{20,}|sk_live_|xox[abpr]-|AIza[0-9A-Za-z_-]{30,}|BEGIN [A-Z ]*PRIVATE KEY|eyJ[A-Za-z0-9_-]{15,}\.eyJ|://[^/:@ ]+:[^/@ ]+@" -- <changed paths>
```

A match is only a candidate. It is a secret when the value is a literal (a real key, token, password or connection string). It is not one when the value is a variable, a function call or a read from the environment (`process.env.X`, `os.getenv`).
Some files are secret by nature, whatever they contain:

- `.env` and `.env.*` (but not `.env.example`, `.env.sample` or `.env.template`)
- `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `id_rsa*`
- `credentials*.json`, `service-account*.json`, `*.tfstate`
- `.npmrc` or `.pypirc` when they contain tokens

When you find a secret:

- Leave the file out. If it's already staged, run `git restore --staged <path>`.
- Tell the user the file and the line, with the value masked (`sk-…3xQ`). Never repeat the full value.
- Suggest moving the value into an environment variable and adding the file to `.gitignore`.
- If the secret was already in an earlier commit, tell the user it must be rotated. Removing it from the code does not remove it from history.

**Leftovers** are new files that don't belong to the change:

- **Session notes** left behind by a person or an agent: Markdown plans, summaries, reports, TODO lists or scratch files (`PLAN.md`, `NOTES.md`, `SUMMARY.md`, `TODO.md`, `*-notes.md`, `scratch*`…). Treat one as a leftover when nothing in the project links to it and it reads like working notes rather than documentation.
- **Instruction files** that are the product, not documentation: `SKILL.md`, `AGENTS.md`, `CLAUDE.md`, rules read by an agent, templates. Their changes go to step 4 (type decision), not `docs`.
- **Temporary or generated files:**
  - logs and temp files: `*.log`, `*.tmp`, `*.bak`, `*.orig`, `*.rej`, `*.swp`, `*~`
  - OS files: `.DS_Store`, `Thumbs.db`
  - dumps and archives: `*.zip`, `*.tar.gz`
  - build output: `dist/`, `build/`, `coverage/`
  - dependency folders: `node_modules/`, `.venv/`
- **Personal settings:** `*.local.*`, `.claude/settings.local.json`, and editor folders (`.idea/`, `.vscode/`) unless the repository already versions them.
- **Paths excluded by the user** (e.g., "only code, not docs"). Treat as leftovers and list them at the end.

Don't stage leftovers, and never delete them. List them in one line at the end. If they keep showing up, offer a separate `🙈 chore` commit that adds them to `.gitignore`.

## 3. Group

- Each commit holds one functional intent that can be reviewed or reverted on its own.
- Use as few commits as possible without mixing intents. Avoid artificially tiny commits and giant mixed ones alike.
- Tests, docs, config and dependencies that exist *for* a change go in the same commit as that change. A manifest and its lockfile always go together.
- If a refactor enables a feature, commit the refactor first and the feat second.
- Keep what the user already staged unless they asked you to regroup.

If there is more than one group, show the plan as one line per commit (title and files), then proceed.

**Handling mixed changes in one file:** If one file has changes for different intents, extract the relevant hunks manually. Generate the diff with context (`-U3` or `-U1 --inter-hunk-context=0`), apply hunks selectively to a copy of the original, verify the copy (structure intact), then stage via `git update-index --cacheinfo` without touching the working tree. Never use `--unidiff-zero` to insert lines without context.

## 4. Type

Ask these about the group being committed, in order. Each one is a yes/no question about the changed paths and the diff, never about how the change feels. **The first `yes` decides the type. Stop there.**

1. Does the group undo an earlier commit? → `revert`

2. Is *every* changed path documentation (`*.md` for user-facing docs, `docs/`, API reference) or a comment inside code?
   - Yes → `docs`
   - *Example:* README update, API docs, inline docblock. Not: `SKILL.md` (instruction file).

3. Is *every* changed path a test, mock, fixture or snapshot?
   - Yes → `test`
   - *Example:* `test_*.py`, mocks, fixtures. Not: production code with tests added.

4. Is *every* changed path a CI/CD pipeline file (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)?
   - Yes → `ci`
   - *Example:* GitHub workflow added. Not: script called by CI.

5. Is *every* changed path build, packaging or dependency (manifest, lockfile, bundler config, Dockerfile)?
   - Yes → `build`
   - *Example:* `package.json`, `Dockerfile`, `pyproject.toml`. Not: test runner config (→ `chore`).

6. Does the diff change what a user or caller can observe (output, screen, response, side effect)?
   - 6a. Can someone now do something they could not do before? → `feat`
      - *Example:* new endpoint, new command, new filter, new validation rule, new capability.
   - 6b. Is something that was broken or working incorrectly now fixed? → `fix` (with area gitmoji if it matches)
      - *Examples of `fix`*: button didn't respond now does; calculation was wrong now correct; data was lost now persists.
      - *Examples of `fix` + area gitmoji*: changed business rule (👔 fix), restyled UI (💄 fix), improved flow (🚸 fix), adapted to API change (👽️ fix).
      - *Rule:* Gitmoji describes *what area* changed, type describes *why* (it was broken and we fixed it, or we intentionally changed it per policy). Consult [references/gitmojis.md](references/gitmojis.md) "Use for" to match.
   - 6c. Does nothing else apply? → `chore` (config, tooling, release, seeds, logs).

7. Behavior is identical. Is it measurably faster or lighter? → `perf`

8. Behavior is identical. Is the diff formatting only (whitespace, lint autofix, import order)? → `style`

9. Behavior is identical. Is code restructured (extract, rename, move, simplify, dead code removed)? → `refactor`

10. Nothing matched? → `chore` (last resort, never a catch-all).

**Rules resolving ties:**

1. Steps 2–5 need *every* path to qualify. One production or instruction file sends it to step 6.
2. Step 6a is about capability, not size. A one-line option nobody had is `feat`; a rewritten screen doing the same is `refactor` or `style`.
3. Breaking change (removed/renamed API, incompatible contract/config): type stays as above, gitmoji becomes 💥, add `!` after scope and `BREAKING CHANGE:` footer.

## 5. Gitmoji

The gitmoji is looked up, never recalled. [references/gitmojis.md](references/gitmojis.md) holds all 75, grouped by type, and is the only source of truth. Run these steps with the file open:

1. **Default.** Take the default gitmoji of the type from section 4: `feat` ✨ · `fix` 🐛 · `refactor` ♻️ · `perf` ⚡️ · `style` 🎨 · `docs` 📝 · `test` ✅ · `build` 📦️ · `ci` 👷 · `chore` 🔧 · `revert` ⏪️.

2. **Candidate.** Look through the catalog, starting with the section for that type. If one row's *Use for* column describes the whole commit, it becomes the candidate. If none does, keep the default.

3. **Check the pair.** The candidate's *Type* must equal the type from section 4. If it does, use it.

4. **Exception, or nothing.** If the candidate's *Type* differs, the pair is valid only when the row's *Exception* names your type **and** the condition is literally true for this diff. When not, discard and go back to the default.

5. **Breaking change.** If the change breaks consumers, gitmoji becomes 💥 and header carries `!`. This replaces the steps above.

**`feat` always takes ✨.** The official catalog gives every gitmoji a `semver` level. Only ✨ is `minor` (for `feat`), only 💥 is `major`; the rest are `patch` or `null`. Whatever area a change touches, if it adds capability, it is `✨ feat`.

Two things are never allowed: a pair not in the catalog, and a gitmoji chosen from memory without opening the file. 🚧 💩 🍻 stay out of shared history.

## 5b. Validate before writing the message

For each commit, and before a single word of the message is written, confirm out loud, in one line:

```
<gitmoji> + <type> → row found in references/gitmojis.md, column Type = <type>  ✔
```

If the row's *Type* column does not literally contain the type, the pair is invalid: go back to section 5 and take the default. A commit is never created on a pair that was not read from the table in this session.

## 6. Language

Go through these in order and stop at the first that applies. It works for any language.

1. The user states a language.
2. An existing convention file states one.
3. The majority language of the `git log` subjects. If history switched languages, the recent commits win.
4. There is no history, or it is mixed: use the README's language. Failing that, use the language the user writes to you in.

History outranks the language of the conversation, so commits stay consistent.
The title and body use that language. The gitmoji, the type keyword (`feat`, `fix`…), existing scope names and code identifiers stay as they are.

**Programming terms stay in English** in every language, because that is how developers learn and use them. Translating them changes their meaning. Some examples: dashboard, frontend, backend, endpoint, API, webhook, middleware, token, cache, query, payload, deploy, build, release, hotfix, pipeline, branch, merge, pull request, bug, script, framework, layout, responsive, login, feature flag, timeout.
Translate one of them only if the user asks you to. Everyday words are still translated as usual (cart → carrito, invoice → factura).

- ✅ `✨ feat(ventas): resumen del mes en el dashboard`
- ❌ `✨ feat(ventas): resumen del mes en el tablero de control`

## 7. Message

```
<gitmoji> type(scope): title

<body>
```

**Scope** is one lowercase domain: `auth`, `checkout`, `orders`, `notifications`. Never a file, component, class, route or variable name. Scope must match existing scopes in the repository's history.

**Title** is a noun phrase answering "what changed?" the way you'd tell a colleague in one sentence.

- Don't open with a verb: *add, added, fixes, agregar, agrega, ajouter, adicionar, hinzufügen*…
- Concrete, not abstract. "sign-in with Google", not "improved auth"; "faster history for large accounts", not "performance improvement".
- Start lowercase unless history capitalizes or language requires it (German nouns). No trailing period.
- ~50 characters ideal; max 72 (or whatever length history uses).
- Don't repeat the scope.
- Describe the change you made, not the entire feature.

**Title examples: ✅ vs ❌**

| ❌ | ✅ | |
|---|---|---|
| `fix(auth): bug` | `fix(auth): sessions closed after password change` | Specific, says which bug |
| `feat(api): add authentication` | `feat(api): sign-in with Google accounts` | Noun phrase, no verb |
| `perf(orders): Redis cache in OrderService` | `perf(orders): faster history for large accounts` | Effect, not implementation |
| `refactor: improvements` | `refactor(checkout): address validator extracted` | Domain scope, concrete |
| `chore: updated dependencies` | `chore(deps): upgrade React to v18.2` | Specific, not vague |

**Body** says what changed, why, and what the impact is, in prose. Skip it only for trivial commits (typo, formatting, dependency bump).

A small change:

```
🐛 fix(checkout): correct total with stacked coupons

A percentage coupon applied after a fixed-amount one discounted the
original price instead of the reduced one, so customers were charged less
than expected. Discounts now apply in sequence.
```

A large change across related areas:

```
✨ feat(notificaciones): correos sobre el estado del pedido

Los clientes reciben un correo cada vez que su pedido cambia de estado,
sin tener que entrar a su cuenta para revisarlo.

Los cambios principales incluyen:

- Aviso al confirmar, enviar y entregar el pedido.
- Preferencias para desactivar cada tipo de aviso.
- Correos en el idioma de la cuenta del cliente.
```

**Body rules:**
- Explain why, not just what.
- Say impact or effect ("users no longer see X", "queries 10x faster").
- No changelog-style headings, lists of files, line-by-line explanations.
- No metrics unless they're verifiable and relevant ("queries 10x faster", not "much better").
- No AI signature or credit. That includes `Co-Authored-By` naming an AI, session links, model names.

Allowed trailers: `BREAKING CHANGE:`, issue references (`Refs #123`, `Closes #123`), human `Co-authored-by`.

## 8. Commit

Stage each group selectively with `git add <paths>`. Don't use `git add -A` or `git add .` when there are several groups.

Pass the message through a file. This works on every OS and shell and keeps emojis intact:

1. Write the message to `.git/GITMOJI_MSG` with your file tool, as UTF-8 without a BOM. In a worktree or submodule, use the path printed by `git rev-parse --git-path GITMOJI_MSG` instead.
2. Run `git commit -F .git/GITMOJI_MSG`.

If you have no file tool, run `git commit -m "<header>" -m "<paragraph>" -m "<paragraph>"` (each `-m` becomes one paragraph). Keep `"`, `$` and backticks out of the text. On Windows PowerShell 5 or cmd, emojis may get mangled, so prefer the file.

For several commits in succession, write `GITMOJI_MSG_01`, `GITMOJI_MSG_02`… before starting, then delete them when done.

**Before each commit, verify:**

- [ ] **Type**: Ran through section 4 step by step. First yes wins. For step 6c, consulted ambiguous cases below.
- [ ] **Gitmoji**: Looked up pair in catalog. Column *Type* matches. Confirmed aloud.
- [ ] **Scope**: Domain name (not file path). Matches history.
- [ ] **Title**: Noun phrase, no verb. ~50 chars. Doesn't repeat scope.
- [ ] **Body**: Explains why and impact. No headings, lists of files, or metrics unless verifiable.
- [ ] **Contents**: One intent. Revertible on its own. No secrets, temp files, session notes.

**After each commit, extract and check the intermediate commit if you separated hunks:**

If the commit was assembled from intermediate file versions (hunks selected manually), that commit's tree never existed on disk and was never built. Verify it:

1. Extract the commit: `git archive <commit> | tar -x -C <tmp>`.
2. Run the project's typecheck or build (e.g., `npm run build`, `go build`, `python -m py_compile`).
3. If it fails and nothing has been pushed, rewrite from the last clean commit via `git commit -C <previous>` reusing the message, then verify the final tree matches: `git rev-parse HEAD^{tree}`.

Finish with `git log --oneline -n <number of commits made>`.

### Ambiguous cases in step 6

These pairs appear in many codebases. Decide by asking: *was this broken/missing and now works, or did we intentionally change working behavior?*

**Database schema:** Adds columns for new feature (→ goes in that feature's `feat` commit). Fixes data corruption or backfills missing data (→ `🗃️ fix`). Restructures for performance (→ `⚡️ perf` or `🗃️ fix`).

**API adaptation:** External API we use changed format; we adapt (→ `👽️ fix`). Their bug; they fixed it, we remove workaround, result identical (→ `♻️ refactor`).

**Validation:** New rule didn't exist (→ `✨ feat`). Change existing rule per policy (→ `🦺 fix`). Typo in validation message (→ `💬 fix`).

**UI or visual:** Broken on mobile/darkmode, now works (→ `📱 fix` or `💄 fix`). Restyling, changing colors, improving layout (→ `💄 fix`). Improved usability, fewer steps, clearer copy (→ `🚸 fix`).

## 9. Special cases

- **Nothing to commit.** Say so and stop.
- **A merge, rebase or cherry-pick in progress** (`git status` says so). Don't commit on top of it; tell the user.
- **The user supplies a message.** Keep its meaning and adapt it to the format.
- **First commit of a repository.** `🎉 chore(project): <what the project is>`.
- **Revert.** Run `git revert --no-commit <hash>`, then commit as `⏪️ revert(scope): <title of the reverted commit>`. The body names the hash and reason.
- **Amend.** Only if the user asks and the commit has not been pushed.
- **Breaking change:** Criteria: removed or renamed API path/field, field type changed, parameter required when optional, behavior by default different. Type stays as above, gitmoji becomes 💥, add `!` after scope, include `BREAKING CHANGE: <what consumers must change>` in body.
