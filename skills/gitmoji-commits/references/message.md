# Writing the message: details and examples

Read this when writing the body of a `feat`, `fix` or breaking change, or when a title does not come easily. SKILL.md step 7 has the rules; this file has the reasoning and the examples.

## Scope

One lowercase domain: `auth`, `checkout`, `orders`, `notifications`.

- Never a file, component, class, route, table or variable name.
- A technical layer (`schema`, `db`, `api`, `ui`, `backend`) is not a domain. Use the business domain the change belongs to (`empresas`, `pagos`), unless history already uses that layer consistently.
- Reuse a scope from history when one fits. Create one only for a new area.
- Monorepo: when history scopes by package (`web`, `api`, `packages/ui`), follow it.
- Cross-cutting changes with no single domain: `project`, `deps`, `config`, `release`, or omit the scope if history does.

## Title

A noun phrase that answers "what changed?" the way you would tell a colleague.

| ❌ | ✅ | Why |
|---|---|---|
| `🐛 fix(auth): bug` | `🐛 fix(auth): sessions closed after a password change` | Says which bug |
| `✨ feat(api): add authentication` | `✨ feat(auth): sign-in with Google accounts` | Noun phrase, domain scope |
| `⚡️ perf(orders): Redis cache in OrderService` | `⚡️ perf(orders): faster history for large accounts` | The effect, not the implementation |
| `♻️ refactor: improvements` | `♻️ refactor(checkout): address validator extracted` | Concrete |
| `✨ feat(dashboard): new dashboard charts` | `✨ feat(dashboard): monthly sales by category` | Scope not repeated |
| `🔧 chore: updated dependencies` | `⬆️ build(deps): React 18.2` | Right type, no verb |
| `✨ feat(ventas): resumen en el tablero de control` | `✨ feat(ventas): resumen del mes en el dashboard` | Programming terms stay in English |

The same rules in other languages:

```
🐛 fix(carrito): total correcto con cupones combinados
♻️ refactor(panier): calcul des remises dans un seul service
⚡️ perf(relatorios): exportação sem bloquear a interface
✨ feat(suche): Filter nach Preis und Marke
```

## Body by type

The reader is a teammate who was not in the session, does not know the domain, and has only `git log`.

| Type | The body answers |
|---|---|
| `feat`, `fix` | **Before**: what was missing or wrong, and what it caused. **Now**: what the user does or sees, told as a flow, with fallbacks step by step. **Why it matters**: fewer errors, less support, no manual step. |
| `refactor` | What made the old structure hard to work with, what the new structure is, what it makes easier. Say explicitly that behavior is unchanged. |
| `perf` | What was slow and for whom, the measured before and after and how it was measured, what changed to get there. |
| `build` (deps) | Why the upgrade: security advisory, needed fix or feature, end of life. Anything a developer must do after pulling. |
| `revert` | The reverted hash and title, what went wrong, what happens next. |
| `docs`, `style`, `test`, `ci`, `chore` | Optional. One or two sentences when the reason is not obvious from the title. |

A technical detail (endpoint, cache time, limit) goes in only with its reason: "the link expires after 24 hours because the file holds customer data". A detail without a reason is noise.

The test: after reading the commit, could that teammate explain the change to someone else? If not, rewrite it. Packing facts into short sentences and parentheses makes a body shorter, not clearer.

### A feature

```
❌ ✨ feat(reports): background export

   Exports over 5,000 rows go to a queue (ExportJob, 24 h link). Under
   that, direct download. Failures notify by email.

✅ ✨ feat(reports): large exports delivered by email

   Exporting a big report froze the page for minutes and often ended in
   a timeout, so users split it by date and exported it in parts.

   Reports over 5,000 rows are now prepared in the background: the user
   keeps working and gets an email with a download link when the file is
   ready. Smaller reports still download right away, as before. The link
   expires after 24 hours because the file holds customer data.

   If the export fails, the email says so and offers a retry, so nobody
   waits for a file that will never arrive.
```

The ❌ title names the mechanism, and its body lists rules without saying what was wrong before, why the link expires, or what the user sees when it fails.

### A small fix

```
🐛 fix(checkout): correct total with stacked coupons

A percentage coupon applied after a fixed-amount one discounted the
original price instead of the reduced one, so customers were charged less
than expected. Discounts now apply in sequence.
```

### A refactor

```
♻️ refactor(orders): totals calculated in one place

Cart, checkout and invoices each computed taxes and discounts with their
own copy of the rules, and the copies had started to drift. All three now
call `calculateTotals`, so a rule change happens once. Totals are
identical to before for every existing order.
```

### A performance change

```
⚡️ perf(orders): faster history for large accounts

Accounts with more than 10,000 orders waited around 8 seconds for the
order history, measured on the staging copy of production. Orders are now
loaded by page with an index on `customer_id, created_at`, and the same
page opens in about 300 ms. Results and sorting are unchanged.
```

### A large change across related areas

```
✨ feat(notificaciones): correos sobre el estado del pedido

Los clientes reciben un correo cada vez que su pedido cambia de estado,
sin tener que entrar a su cuenta para revisarlo. Con esto llegan:

- Aviso al confirmar, enviar y entregar el pedido.
- Preferencias para desactivar cada tipo de aviso.
- Correos en el idioma de la cuenta del cliente.
```

## Body rules

- **Self-contained.** No "see…", "ver…", "voir…", "as explained", "check the docs", "(ver X)". If something matters, write it in the body. If a file truly holds the details, give its path from the repository root (`docs/deploy.md`) and say what it holds.
- **Plain words.** Name things the way the code or the user does. A term only the session invented ("the new pipeline", "phase 2 handler") means nothing to the reader: use the real identifier in backticks (`POST /invoices/{id}/send`, `SMTP_HOST`) or describe the effect.
- No section headings ("Changes:", "Summary:"), no lists of files, no line-by-line explanations. A short list of behaviors is fine for large changes.
- Metrics only when measured and relevant, with how they were measured.
- Wrap at 72 characters. One blank line between paragraphs. URLs and code may run longer.
- No AI signature or credit: no `Co-Authored-By` naming an AI, no "Generated with", no session links, no model names, no 🤖.

## Trailers

Allowed, after one blank line at the end: `BREAKING CHANGE:`, issue references (`Refs #123`, `Closes #123`), human `Co-authored-by`, and any trailer the repository's convention requires (`Signed-off-by` for DCO).

## `BREAKING CHANGE:` footer

For whoever must update their deploy or client. One footer per break, each with the real name and exactly what they must do:

```
❌ BREAKING CHANGE: some fields and flags changed (see the migration
   guide). Old exports are no longer supported by the new flow.

✅ BREAKING CHANGE: user responses no longer include `fullName`; read
   `firstName` and `lastName` and join them on the client.
✅ BREAKING CHANGE: the CLI flag `--out` is now `--output`; scripts
   that pass `--out` fail with "unknown option".
```

The ❌ version mixes several breaks, sends the reader to a guide without saying where it is, and names nothing a consumer could search for.
