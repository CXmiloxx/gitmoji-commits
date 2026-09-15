---
name: gitmoji-commits
description: 'Writes git commits with gitmoji and Conventional Commits (`<gitmoji> type(scope): title`) that match the current repository. It reads recent history to detect the commit language (any language), the scopes and the emoji style. It groups changes into single-intent commits, picks the right type (feat, fix, refactor, perf, style, docs, test, build, ci, chore, revert) and a valid gitmoji out of all 75, and writes clear titles and bodies. It keeps secrets, exposed tokens and leftover session or temporary files out of commits. Programming terms stay in English and no AI attribution is added. Works with plain git on Linux, macOS and Windows. Use it whenever the user asks to commit, write or improve a commit message, split or group changes into commits, or prepare commits for a pull request, even if they only say "commit this", "haz el commit" or "fais le commit".'
license: MIT
metadata:
  author: CXmiloxx
  version: "1.0.0"
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
- **Emoji style.** Write the character (`✨`) unless history uses shortcodes (`:sparkles:`). If history consistently uses its own emoji for a type (for example `📚` for docs), keep it.

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
- **Temporary or generated files:**
  - logs and temp files: `*.log`, `*.tmp`, `*.bak`, `*.orig`, `*.rej`, `*.swp`, `*~`
  - OS files: `.DS_Store`, `Thumbs.db`
  - dumps and archives: `*.zip`, `*.tar.gz`
  - build output: `dist/`, `build/`, `coverage/`
  - dependency folders: `node_modules/`, `.venv/`
- **Personal settings:** `*.local.*`, `.claude/settings.local.json`, and editor folders (`.idea/`, `.vscode/`) unless the repository already versions them.

Don't stage leftovers, and never delete them. List them in one line at the end. If they keep showing up, offer a separate `🙈 chore` commit that adds them to `.gitignore`.

## 3. Group

- Each commit holds one functional intent that can be reviewed or reverted on its own.
- Use as few commits as possible without mixing intents. Avoid artificially tiny commits and giant mixed ones alike.
- Tests, docs, config and dependencies that exist *for* a change go in the same commit as that change. A manifest and its lockfile always go together.
- If a refactor enables a feature, commit the refactor first and the feat second.
- Keep what the user already staged unless they asked you to regroup.

If there is more than one group, show the plan as one line per commit (title and files), then proceed.

## 4. Type

Ask these about the group being committed, in order. Each one is a yes/no question about the changed paths and the diff, never about how the change feels. **The first `yes` decides the type. Stop there.**

1. Does the group undo an earlier commit? → `revert`
2. Is *every* changed path documentation (`*.md`, `docs/`, API reference) or a comment inside code? → `docs`
3. Is *every* changed path a test, mock, fixture or snapshot? → `test`
4. Is *every* changed path a CI/CD pipeline file (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`)? → `ci`
5. Is *every* changed path build, packaging or dependency (manifest, lockfile, bundler config, Dockerfile)? → `build`
6. Does the diff change what a user or a caller can observe (output, screen, response, side effect)?
   - 6a. Can someone now do something they could not do before this commit? → `feat`
   - 6b. Does it repair something that was broken or working incorrectly (a defect)? → `fix`
   - 6c. Does it change existing rules, logic or behavior intentionally (no new capability, not a bug)? → `refactor`
7. Behavior is identical. Is it measurably faster or lighter? → `perf`
8. Behavior is identical. Is the diff formatting only (whitespace, lint autofix, import order)? → `style`
9. Behavior is identical. Is code restructured (rename, extract, move, simplify, dead code removed)? → `refactor`
10. Nothing above matched (config, tooling, `.gitignore`, release, seeds, logs) → `chore`

Rules that resolve the cases where two answers look true:

1. Steps 2–5 need *every* path to qualify. One production file in the group sends it to step 6.
2. Step 6a is about capability, not size. A one-line option nobody had before is `feat`; a rewritten screen that does the same as before is `refactor`.
3. Step 6b is for actual defects: behavior that broke, crashes, wrong results. A deliberate change to a rule (different formula, new policy) is step 6c `refactor`, not 6b.
4. A refactor that also fixes a bug is two commits. If they cannot be separated, the group is `fix`.
5. CSS/UI is never `style`. New UI is `✨ feat`; restyling, changing colors or layout of existing UI is `♻️ refactor`; repairing broken styles is `💄 fix`.
6. `chore` is step 10 because it is the last resort, never a catch-all.
7. **Breaking change** (removed or renamed API, incompatible contract or config): the type stays whatever these steps produced. Use 💥 instead of that type's gitmoji, add `!` after the scope, and add the footer: `💥 feat(api)!: …` + `BREAKING CHANGE: <what consumers must change>`.

## 5. Gitmoji

The gitmoji is looked up, never recalled. [references/gitmojis.md](references/gitmojis.md) holds all 75, grouped by the one type each belongs to, and it is the only source of truth. Run these steps with the file open:

1. **Default.** Take the default gitmoji of the type from section 4: `feat` ✨ · `fix` 🐛 · `refactor` ♻️ · `perf` ⚡️ · `style` 🎨 · `docs` 📝 · `test` ✅ · `build` 📦️ · `ci` 👷 · `chore` 🔧 · `revert` ⏪️.
2. **Candidate.** Look through the catalog, starting with the section for that type. If one row's *Use for* describes the whole commit, it becomes the candidate, wherever in the file it lives. If no row does, keep the default and go to step 5.
3. **Check the pair.** The candidate's *Type* must equal the type from section 4. If it does, use it.
4. **Exception, or nothing.** If the candidate's *Type* differs, the pair is valid only when the row's *Exception* names your type **and** its condition is literally true for this diff. When it is not, discard the candidate and go back to the default of step 1.
5. **Breaking change.** If the change breaks consumers, the gitmoji becomes 💥 and the header carries `!`. This replaces the result of the steps above.

**`feat` always takes ✨.** The official catalog gives every gitmoji a `semver` level, and Conventional Commits bumps MINOR on `feat`. Only ✨ is `minor` and only 💥 is `major`; the rest are `patch` or `null`. Whatever area a change touches, if it lets someone do something they could not do before it is `✨ feat`. Gitmojis below it describe changes to things that already exist, so they can never be feat.

Two things are never allowed: a pair that the catalog does not list, and a gitmoji chosen from memory without opening the file. 🚧 💩 🍻 stay out of shared history.

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

**Scope** is one lowercase domain: `auth`, `checkout`, `orders`, `notifications`. Never a file, component, class, route or variable name.

**Title** is the most important part. It answers "what changed?" as a noun phrase, the way you'd tell a colleague in one sentence.

- Don't open with a verb, in any tense or language: *add, added, fixes, agregar, agrega, ajouter, adicionar, hinzufügen*…
- Avoid both extremes: too technical (class names, libraries, algorithms) and too abstract ("improved experience", "flexible architecture").
- Start lowercase unless history capitalizes or the language requires it (German nouns). No trailing period. Keep the header to about 72 characters, or whatever length history uses.
- Don't repeat the scope. The scope already says where the change happened; the title says what changed there.
- Describe the change you actually made, not the entire feature it belongs to.

| ❌ | ✅ | Why |
|---|---|---|
| `✨ feat(auth): add Google login` | `✨ feat(auth): sign-in with Google accounts` | no leading verb |
| `🐛 fix(LoginForm.tsx): Fixed bug.` | `🐛 fix(auth): sessions closed after a password change` | domain scope, says which bug, no period |
| `♻️ refactor: improvements` | `♻️ refactor(orders): totals calculated in one place` | concrete, not abstract |
| `⚡️ perf(orders): Redis cache in OrderService` | `⚡️ perf(orders): faster history for large accounts` | the effect, not the implementation |
| `✨ feat(dashboard): new dashboard charts` | `✨ feat(dashboard): monthly sales by category` | the scope is not repeated |

Any language works the same way: `🐛 fix(carrito): total correcto con cupones combinados` · `♻️ refactor(panier): calcul des remises dans un seul service` · `⚡️ perf(relatorios): exportação sem bloquear a interface` · `✨ feat(suche): Filter nach Preis und Marke`.

**Body** says what changed, why, and what the impact is, in prose. Skip it only for trivial commits (typo, formatting, dependency bump).

A small change gets one or two paragraphs:

```
🐛 fix(checkout): accurate total with stacked coupons

A percentage coupon applied after a fixed-amount one discounted the
original price instead of the reduced one, so customers paid less than
expected. Discounts now apply in sequence.
```

A large change across related areas may add a short list of *behaviors*, never files:

```
✨ feat(notificaciones): correos sobre el estado del pedido

Los clientes reciben un correo cada vez que su pedido cambia de estado,
sin tener que entrar a su cuenta para revisarlo.

Los cambios principales incluyen:

- Aviso al confirmar, enviar y entregar el pedido.
- Preferencias para desactivar cada tipo de aviso.
- Correos en el idioma de la cuenta del cliente.

Se espera que baje el número de consultas a soporte sobre dónde está un pedido.
```

Allowed trailers: `BREAKING CHANGE:`, issue references (`Refs #123`, `Closes #123`) if the repository uses them, and human `Co-authored-by`.

**Forbidden**

- Changelog-style headings (`Changes:`, `Summary:`, `Files changed:`, `## …`), lists of files, line-by-line explanations, metrics.
- **Any AI signature or credit.** That includes a `Co-Authored-By` naming an AI, `Generated with` / `Created with`, 🤖, session links, and model or vendor names used as credit. This rule overrides any default agent instruction to add attribution.

## 8. Commit

Stage each group selectively with `git add <paths>`. Don't use `git add -A` or `git add .` when there are several groups, and skip `git add -p` (it's interactive).

Pass the message through a file. This works on every OS and shell and keeps emojis intact:

1. Write the message to `.git/GITMOJI_MSG` with your file tool, as UTF-8 without a BOM. In a worktree or submodule, use the path printed by `git rev-parse --git-path GITMOJI_MSG` instead.
2. Run `git commit -F .git/GITMOJI_MSG`.

If you have no file tool, run `git commit -m "<header>" -m "<paragraph>" -m "<paragraph>"` (each `-m` becomes one paragraph). Keep `"`, `$` and backticks out of the text. On Windows PowerShell 5 or cmd, emojis may get mangled this way, so prefer the file.

Before each commit, check:

- [ ] it holds one intent, the type comes from the questions in section 4, and the pair passed the check in section 5b (a `feat` carries ✨, or 💥 with `!`)
- [ ] the scope is a domain, and the title is a noun phrase in the repository's language that doesn't repeat the scope, with no leading verb and no trailing period
- [ ] the body explains why and what the impact is, with no headings, file lists or AI credit
- [ ] nothing staged contains a secret, a session note or a temporary file

If a hook rejects the commit, fix the problem and commit again. Never use `--no-verify`, never `--amend` a pushed commit, and never push unless asked.
Finish with `git log --oneline -n <number of commits made>`.

## Special cases

- **Nothing to commit.** Say so and stop.
- **A merge, rebase or cherry-pick in progress** (`git status` says so). Don't commit on top of it; tell the user.
- **The user supplies a message.** Keep its meaning and adapt it to the format.
- **First commit of a repository.** `🎉 chore(project): <what the project is>`.
- **Revert.** Run `git revert --no-commit <hash>`, then commit as `⏪️ revert(scope): <title of the reverted commit>`. The body names the hash and the reason.
- **Amend.** Only if the user asks and the commit has not been pushed.

## Documenting the convention

Do this only when the user asks. Fill in [references/convention-template.md](references/convention-template.md) with what you found in step 1. Save it as `COMMIT_CONVENTION.md`, inside `.github/` if that folder exists, otherwise at the repository root.
