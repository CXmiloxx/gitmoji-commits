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

What changed, why, and the impact, in prose. A short list of behaviors is allowed for large changes. Never file lists, changelog headings or AI credit.
<!-- trailers the project uses, e.g. "Refs #123" -->

## Grouping

One functional intent per commit. Tests, docs and dependencies that exist for a change travel with it.
```
