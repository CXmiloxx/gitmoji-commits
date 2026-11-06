# Splitting one file across commits

Read this when a single file holds changes for two intents (a bug fix and a feature in the same file). Interactive `git add -p` is not available to an agent; stage hunks with a patch instead. Only git is used, so it works on every OS.

`<dir>` below is the directory of the path printed by `git rev-parse --git-path GITMOJI_MSG` (usually `.git`).

## Stage part of a file

1. Write the file's diff to a patch, with context:

   ```
   git diff -U3 --output=<dir>/GITMOJI_PATCH -- <file>
   ```

   `--output` avoids shell redirection, which PowerShell 5 writes as UTF-16 and corrupts.

2. Open `<dir>/GITMOJI_PATCH` with your file tool and keep only the hunks of the intent you are committing:
   - Delete whole hunks (from one `@@` line to the next) that belong to the other intent. Keep the `diff --git`, `---` and `+++` header lines.
   - If one hunk mixes both intents, edit inside it: delete the `+` lines you don't want, and turn the `-` lines you don't want into context by replacing the leading `-` with a space. Never touch context lines.
   - Don't fix the `@@` line counts by hand; `--recount` does it.

3. Check, then stage. The working tree is not touched:

   ```
   git apply --cached --recount --check <dir>/GITMOJI_PATCH
   git apply --cached --recount <dir>/GITMOJI_PATCH
   ```

   If `--check` fails, regenerate the patch from step 1 and edit again. Never use `--unidiff-zero`.

4. Confirm what is staged and what is left:

   ```
   git diff --cached -- <file>
   git diff -- <file>
   ```

   The first shows only this intent; the second shows only the rest.

5. Commit as usual. Then stage the rest of the file normally for the next commit. Delete `GITMOJI_PATCH` when done.

## Verify a commit that never existed on disk

A commit built from part of a file has a tree nobody ever built or ran. When the project has a typecheck, build or fast test command, check that tree in a temporary worktree:

```
git worktree add --detach <tmp> <commit>
```

Run the project's check inside `<tmp>` (for example `npm run build`, `go build ./...`, `python -m compileall -q .`, `cargo check`). Dependencies may need installing there; if that is slow or impossible, say the commit was not verified instead of guessing. Then:

```
git worktree remove --force <tmp>
```

If the check fails and the commit has not been pushed, the commit is missing a hunk it depends on. Add that hunk to the index with the steps above and run `git commit --amend --no-edit` on that commit (if it is not `HEAD`, tell the user and stop: rewriting older commits is their call). Finally make sure the last commit's tree matches the working tree you started from: `git status --short` lists only the files you deliberately left out.
