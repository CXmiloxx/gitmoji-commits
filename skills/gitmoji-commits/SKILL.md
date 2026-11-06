---
name: gitmoji-commits
description: 'Writes git commits with gitmoji and Conventional Commits (`<gitmoji> type(scope): title`) that match the current repository. It reads recent history to detect the commit language (any language), the scopes and the emoji style. It groups changes into single-intent commits, picks the right type (feat, fix, refactor, perf, style, docs, test, build, ci, chore, revert) and a valid gitmoji out of all 75, writes clear titles and bodies, and validates every header with git itself before committing. It keeps secrets, exposed tokens and leftover session or temporary files out of commits. Programming terms stay in English and no AI attribution is added. Works with plain git on Linux, macOS and Windows. Use it whenever the user asks to commit, write or improve a commit message, split or group changes into commits, or prepare commits for a pull request, even if they only say "commit this", "haz el commit" or "fais le commit".'
license: MIT
metadata:
  author: CXmiloxx
  version: "1.0.0"
allowed-tools: Bash(git status:*) Bash(git diff:*) Bash(git log:*) Bash(git ls-files:*) Bash(git rev-parse:*) Bash(git grep:*) Bash(git add:*) Bash(git restore --staged:*) Bash(git apply --cached:*) Bash(git commit -F:*) Read Write
---

# Gitmoji Commits

One commit, one intent, written the way an experienced developer would write it:

```
🐛 fix(auth): sessions closed after a password change

Changing the password left other devices signed in, so a stolen session
kept working. Every active session now ends when the password changes.
```

Only `git` is needed; every command runs the same in bash, zsh, fish, PowerShell and cmd. `<skill>` is the absolute path of this folder. `<dir>` is the folder of the path printed by `git rev-parse --git-path GITMOJI_MSG` (usually `.git`).

## Files

| File | Read it when |
|---|---|
| `references/gitmojis.md` | Step 5, always: only your type's section. |
| `references/types.md` | Step 4 is not obvious, or the change touches a database, external API, validation, permissions, UI or instruction files. |
| `references/message.md` | Writing a body for `feat`, `fix`, `refactor`, `perf` or a breaking change, or a title won't come. |
| `references/splitting.md` | One file holds changes for two intents. |
| `references/special-cases.md` | Hooks, commitlint, gitmoji-cli config, merge in progress, revert, amend, first commit, signing, no file tool, "improve this message", "document the convention". |
| `checks/*.pattern` | Step 8, always, through `git grep`. Never edit them during a commit. |

## Rules that never bend

1. No secret or leftover is staged without the user's explicit confirmation. No user file is deleted.
2. No `--no-verify`, no `--no-gpg-sign`, no `git add -A` / `git add .` when there are several groups.
3. No push unless the user asks. No amend or rewrite of a pushed commit, or of one the user didn't ask you to touch.
4. No commit while a merge, rebase, cherry-pick or revert is in progress.
5. One intent per commit. A security or bug fix never hides inside a `feat`.
6. Every pair comes from the allowlist (step 5) and every message passes the checks (step 8).
7. No AI attribution: no `Co-Authored-By` naming an AI, no "Generated with", no session links, no 🤖.

## Which rule wins

The first source that speaks decides:

1. What the user asks this time. It can't lift rules 1–4, except confirming a flagged file.
2. Written repository rules: commitlint, `COMMIT_CONVENTION.md`, gitmoji-cli config, `CONTRIBUTING*`, hooks.
3. This skill.
4. History, for format only: emoji or shortcode, title case, scopes, language, length. Never a pair.

## 1. Read the repository

Once per session:

```
git status --short --branch
git diff --stat
git diff --cached --stat
git log -n 20 --no-merges --format=%s
git ls-files "*COMMIT_CONVENTION*" "*commitlint*" ".gitmojirc*" "CONTRIBUTING*" ".husky/*" ".pre-commit-config.yaml" "lefthook*"
git grep -n "\"gitmoji\"" -- package.json
git rev-parse --git-path GITMOJI_MSG
```

No commits yet (`git log` fails): new project. A merge, rebase, cherry-pick or revert in progress: stop and tell the user.

Settle, without writing them down:

- **Rules.** Read only the commit section of each file listed. With commitlint or a gitmoji-cli config, read `references/special-cases.md` first.
- **Format.** Character (`✨`) unless history or config uses shortcodes (`:sparkles:`). Spell each gitmoji exactly as the catalog does, variation selector included (`⚡️`, `♻️`, `🗃️`), even if history drops it. Lowercase title start and 72 characters unless history consistently differs.
- **Scopes** from history; a new area gets a new domain name.
- **Issue references.** Only if history uses them: take one from the branch name (`feature/PROJ-42-export` → `Refs PROJ-42`). Never invent one.
- **Invalid pairs in history** (`🗃️ feat`, `📚 docs`): never copied; one line in the report.

Then read the changes with `git diff --no-ext-diff` and `git diff --cached --no-ext-diff`, plus untracked files (`git status --short -uall -- <folder>` for a folder). Lockfiles, minified files, snapshots and binaries are judged by `--stat` only: `git diff --no-ext-diff -- . ":(exclude)*.lock" ":(exclude)*-lock.*" ":(exclude)*.min.*"`. For a large diff, one path at a time.

## 2. Leave out what must not be committed

**Secrets.** Search the changed files:

```
git grep --untracked -n -I -i -E "(api_?key|secret|token|passw|pwd|credential|private_?key|access_?key|auth_?key)[A-Za-z0-9_-]*.{0,3}[:=].{0,3}[A-Za-z0-9/+_-]{16,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_|sk-[A-Za-z0-9_-]{20,}|sk_live_|xox[abpr]-|AIza[0-9A-Za-z_-]{30,}|BEGIN [A-Z ]*PRIVATE KEY|eyJ[A-Za-z0-9_-]{15,}\.eyJ|://[^/:@ ]+:[^/@ ]+@" -- <changed paths>
```

A match is a secret only when the value is a literal, not a variable or an environment read (`process.env.X`, `os.getenv`). Secret by nature: `.env*` (not `.env.example`, `.sample`, `.template`), `*.pem`, `*.key`, `*.p12`, `*.pfx`, `*.jks`, `id_rsa*`, `credentials*.json`, `service-account*.json`, `*.tfstate`, `.npmrc` / `.pypirc` with tokens.

For each: leave it out (`git restore --staged <path>` if staged); report file and line with the value masked (`sk-…3xQ`); suggest an environment variable and a `.gitignore` entry; if an earlier commit already holds it, say it must be rotated.

**Leftovers**, new files that don't belong to the change:

- Session notes nothing links to: `PLAN.md`, `NOTES.md`, `SUMMARY.md`, `TODO.md`, `*-notes.md`, `scratch*`.
- Temporary or generated: `*.log`, `*.tmp`, `*.bak`, `*.orig`, `*.rej`, `*.swp`, `*~`, `.DS_Store`, `Thumbs.db`, `*.zip`, `*.tar.gz`, `dist/`, `build/`, `coverage/`, `node_modules/`, `.venv/`.
- Personal settings not already versioned: `*.local.*`, `.claude/settings.local.json`, `.idea/`, `.vscode/`.
- Paths the user excluded.

Never stage or delete them; list them in the report. Recurring ones: offer a `🙈 chore` commit that ignores them. Instruction files (`SKILL.md`, `AGENTS.md`, `CLAUDE.md`, agent rules, prompt templates) are product, not leftovers.

## 3. Group

- One functional intent per commit, revertible on its own; as few commits as possible.
- **By intent, never by layer.** Migration, model, endpoint, screen, tests and docs of one feature are one `✨ feat`.
- What exists *for* a change goes with it: its tests, docs, config, dependency. Manifest and lockfile together.
- **Staged-only.** If the user staged something and left other changes unstaged, commit only the staged part and list the rest in the report.
- Hunks of two intents in one file: `references/splitting.md`.

A large diff is several intents until proven otherwise: list what it does, one line each; each line with a different type or gitmoji is its own commit. Order: security fixes, bug fixes, enabling refactors, the feature, then standalone docs, build, ci, chore.

With several commits, show the plan in the user's language, then proceed:

```
Plan (3 commits)
1. 🔒️ fix(auth): permission check on invoice export — src/auth/guard.ts
2. ♻️ refactor(invoices): totals calculated in one place — src/invoices/totals.ts
3. ✨ feat(invoices): invoices sent by email — src/invoices/*, tests/invoices/*
Left out: NOTES.md (session notes)
```

## 4. Type

Yes/no questions about the paths and the diff. **The first yes decides.**

1. Undoes an earlier commit? → `revert`
2. **Every** path documentation or code comment? → `docs` (instruction files are not docs)
3. **Every** path a test, mock, fixture or snapshot? → `test`
4. **Every** path a CI/CD pipeline file? → `ci`
5. **Every** path build, packaging or dependency? → `build`
6. Changes what a user or caller observes (output, screen, response, side effect, what an agent does)?
   - a. Someone can do something new → `feat`
   - b. Existing behavior repaired or adjusted on purpose → `fix`
   - c. Neither → `chore`
7. Same behavior, measurably faster or lighter → `perf`
8. Same behavior, formatting only → `style`
9. Same behavior, restructured (extract, rename, move, dead code) → `refactor`
10. Otherwise → `chore`

One production or instruction file sends a group past steps 2–5. Capability decides 6a, not size; 6a beats 6b. The area (database, UI, API) never decides the type. Examples and ambiguous cases: `references/types.md`.

**Breaking change** (removed or renamed field, endpoint, flag or env var; new required parameter; different default): the type stays, the gitmoji becomes 💥, `!` goes before the colon, and the body gets a `BREAKING CHANGE:` footer.

## 5. Gitmoji

Picked **after** the type, **only from its row**. It must describe the intent of the whole commit, not the files touched; the area goes in the scope and title.

| Type | Allowed | Allowed only under the condition in the catalog |
|---|---|---|
| `feat` | ✨ | — |
| `fix` | 🐛 🚑️ 🔒️ 🩹 🥅 👔 💄 🚸 📱 💫 💬 ♿️ 🌐 🔍️ 📈 🛂 🦺 ✈️ 👽️ 🗃️ 🧵 🦖 | 🏷️ 🚨 ✏️ 🍱 🩺 🚩 |
| `refactor` | ♻️ 🏗️ ⚰️ 🗑️ 🏷️ 🔥 🚚 | 🦖 |
| `perf` | ⚡️ | 🗃️ 🧵 |
| `style` | 🎨 🚨 | — |
| `docs` | 📝 💡 ✏️ 👥 | 📄 |
| `test` | ✅ 🧪 🤡 📸 | — |
| `build` | 📦️ ⬆️ ⬇️ 📌 ➕ ➖ 🧱 | 🔧 🔨 |
| `ci` | 👷 💚 🚀 | 🧱 🔐 |
| `chore` | 🔧 🎉 🔖 🙈 🔨 🧑‍💻 🔐 🌱 🔊 🔇 🧐 🍱 🩺 🚩 ⚗️ 💸 🥚 📄 🔀 | 🔥 🚚 👥 🚀 |
| `revert` | ⏪️ | — |
| any type, with `!` | 💥 | breaking change only |

1. Start from the default: the first emoji of the row.
2. Look in `references/gitmojis.md`, **your type's section only**, for a more specific one. It replaces the default only if its *Use for* describes the whole commit: 🗃️ on a `fix` for a broken migration, yes; 🗃️ because a feature touched SQL, no.
3. A conditional one needs its written condition literally true. If you have to argue for it, use the default.
4. A breaking change replaces all of this with 💥.

If the emoji isn't in the row, the emoji is wrong, never the type. `feat` carries only ✨ or 💥. 🚧 💩 🍻 never go into shared history.

## 6. Language

First that applies: what the user asks; a convention file; the majority of `git log` subjects (recent ones win); the README; the user's language.

Title and body use it; gitmoji, type, existing scopes and identifiers don't change. **Programming terms stay in English** unless the user asks otherwise (dashboard, endpoint, API, webhook, token, cache, query, payload, deploy, build, release, pipeline, branch, merge, bug, script, framework, layout, login, feature flag, timeout). Everyday words translate (cart → carrito).

✅ `✨ feat(ventas): resumen del mes en el dashboard` · ❌ `… en el tablero de control`

## 7. Message

```
<gitmoji> <type>(<scope>)<!>: <title>

<body>

<trailers>
```

- **Header.** One space after the gitmoji; lowercase type; lowercase scope without spaces; `!` only with 💥; no space before the colon, one after; no trailing period; 72 characters at most.
- **Scope.** One business domain (`auth`, `checkout`, `pagos`). Never a file, class, route, table or variable; a layer (`db`, `api`, `ui`) only if history uses it consistently.
- **Title.** A noun phrase saying what changed, about 50 characters: "sign-in with Google accounts", not "add Google login". No leading verb in any language, the effect rather than the mechanism, scope not repeated.
- **Body.** Prose for a teammate who has only `git log`; skip it for trivial commits. `feat` / `fix`: what was wrong or missing → what the user does or sees now → why it matters. `refactor`: why, the new structure, behavior unchanged. `perf`: measured before and after, and how. Details only with their reason. No "see X", no session-only terms, no headings, no file lists. Wrap at 72.
- **Trailers.** Only `BREAKING CHANGE:` (one per break: the real name and what consumers must do), issue references, human `Co-authored-by`, and trailers the repository requires (`Signed-off-by`).

Examples for every type: `references/message.md`.

## 8. Validate

**Gate.** Before writing the message, state:

```
<gitmoji> + <type> → allowlist row <type> contains <gitmoji> ✔ (condition: <text or "none">)
```

If the row doesn't literally contain it, back to step 5.

**Checks.** With the message in `<dir>/GITMOJI_MSG`, run (git is only the regex engine here):

```
git -C <dir> grep --no-index -n -h -E -f <skill>/checks/header.pattern -- GITMOJI_MSG
git -C <dir> grep --no-index -n -h -i -E -f <skill>/checks/forbidden.pattern -- GITMOJI_MSG
git -C <dir> grep --no-index -n -h -i -E -f <skill>/checks/review.pattern -- GITMOJI_MSG
```

| Check | Pass |
|---|---|
| `header` | Prints a line starting with `1:`. Nothing printed: malformed header or invalid pair. |
| `forbidden` | Prints nothing. Each line is AI credit, a leading verb, a body heading or a WIP gitmoji: remove it. |
| `review` | Each line is a warning (over 72, "see X", session term, TODO): fix it, or keep it only for a URL, code or a real path. Line 1 over 72 is never kept. |

A convention file that allows an extra pair fails `header` on purpose: check that header by hand against step 7.

## 9. Commit

1. `git add <paths>` for the group (part of a file: `references/splitting.md`).
2. Write `<dir>/GITMOJI_MSG` with your file tool, UTF-8 without BOM (`GITMOJI_MSG_01`, `_02`… for several) and run step 8 on each.
3. `git commit -F <dir>/GITMOJI_MSG`
4. Hook failed: no commit happened. Fix the cause, stage again, commit again; never `--no-verify` or `--amend` for this.
5. `git log -1 --format=%s` must equal the validated header; if a hook rewrote it, validate the new one.
6. At the end, delete the `GITMOJI_MSG*` and `GITMOJI_PATCH` files.

## 10. Report

In the user's language, and nothing else about the process:

```
Commits (2)
a1b2c3d ✨ feat(invoices): invoices sent by email
d4e5f6a 🐛 fix(cart): correct total with stacked coupons

Left out: NOTES.md (session notes) · .env (secret: STRIPE_KEY=sk_…3xQ, line 4)
Notes: history uses `📚 docs`, which is not a gitmoji; it wasn't copied.
```

From `git log --oneline -n <commits made>`. Omit empty lines. Never the full value of a secret.
