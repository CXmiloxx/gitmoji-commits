# Special cases

Read the case that applies. Each one replaces the matching part of the normal flow.

## Repository state

- **Nothing to commit.** Say so and stop.
- **Merge, rebase, cherry-pick or revert in progress** (`git status` says so). Don't commit on top of it. Tell the user what is in progress and stop.
- **Detached HEAD.** Commits made here are easy to lose. Tell the user before committing and suggest a branch.
- **Repository with no commits.** `git log` fails: treat it as a new project. The first commit is `🎉 chore(project): <what the project is>`.
- **Files over 5 MB or binaries outside the usual assets.** Ask before staging them, and mention Git LFS if the repository uses it (`.gitattributes` with `filter=lfs`).
- **Submodules.** A changed submodule pointer is its own `⬆️ build(deps)` commit unless it exists only for a change in the parent repository.

## Repository rules

- **commitlint.** Read `type-enum`, `scope-enum`, `scope-case`, `subject-case`, `header-max-length` and `body-max-line-length`, and follow them. If the config extends `@commitlint/config-conventional` without a gitmoji-aware parser (`commitlint-config-gitmoji`, or a `parserPreset` whose `headerPattern` allows a leading emoji), every header with an emoji will be rejected: tell the user before the first commit and ask whether to drop the emoji or add the parser. Don't decide alone.
- **gitmoji-cli config** (`.gitmojirc.json`, or the `"gitmoji"` key in `package.json`). `"emojiFormat": "code"` means shortcodes (`:sparkles:`), `"emoji"` means characters. `"scopePrompt"` set to a list is the allowed scope list. `"capitalizeTitle"` is `true` by default: when the file exists and doesn't set it to `false`, titles start with a capital letter.
- **`commitlint-config-gitmoji`.** It compares the emoji byte for byte with its own list, so write every gitmoji exactly as `references/gitmojis.md` shows it, variation selector included (`⚡️`, not `⚡`). Its list may not include 🦖 yet, and its shortcode pattern can't parse `:t-rex:`: in that repository, use the type's default gitmoji instead of 🦖.
- **A convention file allows a pair outside the allowlist.** Use it. `checks/header.pattern` will reject that header: that failure is expected, so check the rest of the header by hand.
- **Signed commits** (`commit.gpgsign` true). If signing fails, tell the user. Never pass `--no-gpg-sign` or change the config.
- **DCO** (`Signed-off-by` in history or required by CONTRIBUTING). Commit with `git commit -s -F …`.

## Hooks

- **A pre-commit or commit-msg hook fails.** The commit did not happen. Read the hook output, fix the cause (lint error, failing test, header rejected), stage again and run the same `git commit -F` again. Never use `--no-verify`. Never `--amend` here: there is no new commit to amend, and amending would rewrite the previous one.
- **A hook modified files** (formatter, lint autofix) and the commit did not happen: stage those same files again and commit again.
- **A hook modified files and the commit happened anyway:** the formatter changes stay unstaged. Commit them as `🎨 style` only if they are not part of the next group.
- **A hook rewrote the message** (`prepare-commit-msg`, commitizen). Read the real header with `git log -1 --format=%s` and validate it.
- **The fix the hook asks for is outside the change** (unrelated test failing on `main`). Tell the user. Don't fix unrelated code inside this commit.

## Requests

- **The user supplies a message.** Keep its meaning, adapt it to the format, and show what changed.
- **"Commit everything as one."** The title follows the main intent; the body names every other intent, so no security fix or bug fix hides inside a `feat`.
- **"Only code, not docs"** or any exclusion. Treat excluded paths as leftovers and list them at the end.
- **Amend.** Only if the user asks and the commit has not been pushed (`git status` shows the branch ahead of its upstream, or there is no upstream).
- **Revert.** Run `git revert --no-commit <hash>`, then commit as `⏪️ revert(<scope of the reverted commit>): <title of the reverted commit>`. The body names the hash and the reason.
- **Improve a message only** (no commit). Return the rewritten message and its gate line. Don't stage or commit anything.
- **Rewrite older commits.** Only on explicit request, only for commits not pushed, and say which hashes will change before doing it.
- **Document the convention.** Fill `references/convention-template.md` with what the repository shows and save it as `COMMIT_CONVENTION.md`. Commit it as `📝 docs(project): commit convention`.
- **Push.** Never as part of this skill. If the user asks, push after the commits are made and report the result.

## Tools

- **No file tool.** `git commit -m "<header>" -m "<paragraph>" -m "<paragraph>"`, one `-m` per paragraph, with no `"`, `$` or backticks in the text. On Windows PowerShell 5 or cmd, emojis may break, so prefer the file. Validate the same text by writing it with the shell's own file command only if it writes UTF-8; otherwise check the header by hand against SKILL.md step 7.
