# Convention template

Fill in every `<…>` with what the repository's history and files show, and delete the comments.
Write the whole document in the commit language.

```markdown
# Commit convention

Format: `<gitmoji> type(scope): title`.

## Language

Commits are written in <language>. Gitmojis, types and scopes stay as they are.
Programming terms stay in English (dashboard, endpoint, deploy, token, cache…). They are translated only when someone explicitly asks for it.

## Types

| Type | Gitmoji | When |
|---|---|---|
<!-- one row per type the project uses, default gitmoji first; add the specific
     gitmojis seen in history (e.g. 💄, 🗃️, ⬆️) with a one-line "when" -->

`feat` always uses ✨. Area gitmojis (🌐, 🛂, 🚸…) never go with `feat`: a feature that adds a language or a role is still `✨ feat`.

A breaking change uses 💥 and `!`: `💥 feat(api)!: …` plus a `BREAKING CHANGE:` footer.

## Scopes

| Scope | Covers |
|---|---|
<!-- the scopes already used in history, plus the project's main modules/domains -->

Scopes are lowercase domains, never files, components or classes.

## Title

A noun phrase that says what changed, without repeating the scope, with no leading verb, <lowercase|capitalized> start, no trailing period, about <72> characters for the whole header.

- `<3 real good examples from this repository's history, or written in its style>`

## Body

What changed, why, and the impact, in prose, wrapped at 72 characters. It must make sense with only `git log`: no "see X" pointers. A short list of behaviors is allowed for large changes. Never file lists, changelog headings or AI credit.
Each `BREAKING CHANGE:` footer names one break and what consumers must do.
<!-- trailers the project uses, e.g. "Refs #123" -->

## Grouping

One functional intent per commit, never one layer per commit. The migration, code, tests and docs of a change travel together.
```
