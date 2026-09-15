# Gitmoji catalog

All 75 gitmojis. This file is the only source of truth for which type a gitmoji may carry.

- **Type** is the one type the gitmoji belongs to. Use it unless the Exception applies.
- **Exception** is the only other type allowed, and the literal condition that must be true to use it. `—` means there is no second type.
- Any pair that is not in this table is invalid. Do not derive a pair from memory, from the emoji's name or from another project's convention.

**`feat` only pairs with ✨ and 💥.** The official gitmoji catalog gives every gitmoji a `semver` level, and Conventional Commits bumps MINOR on `feat`. Only ✨ is `minor` and only 💥 is `major`; every other gitmoji is `patch` or `null`, so pairing one with `feat` claims a version bump the gitmoji does not carry. A change that lets someone do something they could not do before is `✨ feat`, whatever area it touches. Every gitmoji below it describes a change to something that already exists.

`⚡️` and `⚡` (with or without the variation selector) are the same gitmoji.

## feat

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| ✨ | `:sparkles:` | feat | — | A capability that did not exist before: new screen, endpoint, option, command, integration, new UI, a new supported language, a new permission, a new validation rule. **The only feat gitmoji.** |

## fix

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 🐛 | `:bug:` | fix | — | A behavior that was supposed to work and did not: wrong result, crash, broken flow. **default fix** |
| 🚑️ | `:ambulance:` | fix | — | Urgent fix shipped straight to production because something critical is down or losing data. |
| 🔒️ | `:lock:` | fix | — | Closing a security or privacy hole: injection, leaked data, missing auth check, unsafe defaults. |
| 🩹 | `:adhesive_bandage:` | fix | — | Small, non-critical fix: an edge case, a minor glitch. |
| 🥅 | `:goal_net:` | fix | — | Catching and handling errors that previously escaped. |
| 🗃️ | `:card_file_box:` | fix | `perf` if the only goal is speed (index, query plan, fewer round trips) | Database changes: schema, migrations, indexes, queries whose essence is the data layer. |
| 🧵 | `:thread:` | fix | `perf` if the commit makes it measurably faster or lighter | Concurrency, multithreading, async coordination, locks, queues. |

## refactor

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| ♻️ | `:recycle:` | refactor | — | Restructuring code without changing what it does: extract, rename, simplify, reorganize. **default refactor** |
| 🏗️ | `:building_construction:` | refactor | — | Architectural changes: layers, boundaries, module structure, patterns across the codebase. |
| ⚰️ | `:coffin:` | refactor | — | Removing dead code that nothing references. |
| 🗑️ | `:wastebasket:` | refactor | — | Deprecating code that will be removed later (marking, warnings, migration notes). |
| 🏷️ | `:label:` | refactor | `fix` if the wrong typing let a real defect through | Type definitions and typings (TypeScript types, interfaces, schemas for types). |
| 🔥 | `:fire:` | refactor | `chore` if every removed path is config, tooling or an asset | Removing code or files that are no longer needed. Removing a public capability is a breaking change: use 💥 instead. |
| 🚚 | `:truck:` | refactor | `chore` if only config, docs or asset paths moved | Moving or renaming files, folders, routes or modules. |
| 👔 | `:necktie:` | refactor | — | Business rules and domain logic: changing calculations, policies, workflows of the domain. **use when step 6c applies** |
| 💄 | `:lipstick:` | refactor | `fix` if repairing broken styles | Visual changes to existing UI: styles, themes, colors, layout, spacing, fonts. |
| 🚸 | `:children_crossing:` | refactor | — | Usability improvements: fewer steps, clearer wording, better feedback to user. |
| 💬 | `:speech_balloon:` | refactor | — | Changing user-facing text, copy, messages or literals that already exist. |
| 🛂 | `:passport_control:` | refactor | — | Authorization, roles and permissions: adding new roles, changing access rules. |
| 🦺 | `:safety_vest:` | refactor | — | Input validation and data validation rules: new validation checks, changing existing rules. |
| ✈️ | `:airplane:` | refactor | — | Offline support, caching for offline use, sync on reconnect. |
| 👽️ | `:alien:` | refactor | — | Adapting to a change in an external API or third-party service. |
| 🦖 | `:t-rex:` | refactor | — | Backwards compatibility: shims, polyfills, keeping old clients working. |
| 📱 | `:iphone:` | refactor | — | Responsive design and mobile layouts. |
| 💫 | `:dizzy:` | refactor | — | Animations and transitions. |
| ♿️ | `:wheelchair:` | refactor | — | Accessibility: keyboard navigation, ARIA, contrast, screen-reader support. |
| 🌐 | `:globe_with_meridians:` | refactor | — | Translations, locales, date/number formatting per locale. |
| 🔍️ | `:mag:` | refactor | — | SEO: meta tags, sitemaps, structured data, indexability. |
| 📈 | `:chart_with_upwards_trend:` | refactor | — | Analytics, tracking events, metrics instrumentation. |

## perf

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| ⚡️ | `:zap:` | perf | — | Measurably faster or lighter code with the same observable result. **default perf** |

## style

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 🎨 | `:art:` | style | — | Formatting or code-structure changes with zero behavior change: whitespace, import order, lint autofix, prettier run. Never for CSS/UI. **default style** |
| 🚨 | `:rotating_light:` | style | `fix` if silencing the warning changes behavior, because it reported a real defect | Silencing compiler or linter warnings. |

## docs

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 📝 | `:memo:` | docs | — | README, guides, ADRs, API docs, changelog prose written by hand. **default docs** |
| 💡 | `:bulb:` | docs | — | Comments inside source code (docblocks, explanatory comments). |
| ✏️ | `:pencil2:` | docs | `fix` if the typo is outside documentation: a code identifier, a user-facing string or a config value | Typos. |
| 👥 | `:busts_in_silhouette:` | docs | `chore` if the file is tooling, such as CODEOWNERS | Contributors lists and maintainers. |

## test

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| ✅ | `:white_check_mark:` | test | — | Adding, updating or fixing tests without touching production code. **default test** |
| 🧪 | `:test_tube:` | test | — | Adding a failing test on purpose (reproducing a bug before fixing it, TDD red step). |
| 🤡 | `:clown_face:` | test | — | Mocks, stubs, fakes and fixtures for tests. |
| 📸 | `:camera_flash:` | test | — | Snapshot files for tests. |

## build

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 📦️ | `:package:` | build | — | Build system, packaging, compiled artifacts, Dockerfiles, bundler output. **default build** |
| ⬆️ | `:arrow_up:` | build | — | Upgrading one or more dependencies. |
| ⬇️ | `:arrow_down:` | build | — | Downgrading one or more dependencies. |
| 📌 | `:pushpin:` | build | — | Pinning dependencies to exact versions. |
| ➕ | `:heavy_plus_sign:` | build | — | Adding a dependency on its own. If the dependency exists only to implement a feature, it belongs to that feat commit. |
| ➖ | `:heavy_minus_sign:` | build | — | Removing a dependency. |
| 🧱 | `:bricks:` | build | `ci` if the changed file is part of the deploy pipeline | Infrastructure: IaC, container orchestration, cloud resources, networking. |

## ci

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 👷 | `:construction_worker:` | ci | — | Adding or changing CI configuration: workflows, jobs, runners, caches. **default ci** |
| 💚 | `:green_heart:` | ci | — | Repairing a broken CI pipeline. |
| 🚀 | `:rocket:` | ci | `chore` if the change touches only release scripts that live outside the pipeline | Deployment configuration or deploy-only changes. |

## chore

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 🔧 | `:wrench:` | chore | `build` if the config file drives the build (bundler, compiler, packaging) | Configuration files: linters, editors, tsconfig, environment defaults. **default chore** |
| 🎉 | `:tada:` | chore | — | The very first commit of a project. Only once per repository. |
| 🔖 | `:bookmark:` | chore | — | Release commits: version bump, release notes, tags. |
| 🙈 | `:see_no_evil:` | chore | — | Changes to .gitignore (or other ignore files). |
| 🔨 | `:hammer:` | chore | `build` if the script runs as part of the build | Development scripts: Makefile targets, npm scripts, local tooling. |
| 🧑‍💻 | `:technologist:` | chore | — | Developer experience: faster local setup, better tooling, dev containers. |
| 🔐 | `:closed_lock_with_key:` | chore | `ci` if the secrets are wired inside a pipeline file | Encrypted secrets, secret templates (.env.example) or secret-manager wiring. Never commit a real secret. |
| 🌱 | `:seedling:` | chore | — | Seed data for databases or local environments. |
| 🔊 | `:loud_sound:` | chore | — | Adding or improving logs. |
| 🔇 | `:mute:` | chore | — | Removing logs. |
| 🧐 | `:monocle_face:` | chore | — | Data exploration and inspection (notebooks, queries, analysis scripts). |
| 🍱 | `:bento:` | chore | `fix` if the asset replaces one that was broken or wrong | Static assets: images, icons, fonts, media. |
| 🩺 | `:stethoscope:` | chore | `fix` if the healthcheck was reporting the wrong state | Healthchecks and readiness/liveness probes. |
| 🚩 | `:triangular_flag_on_post:` | chore | `fix` if changing the flag repairs broken behavior | Adding, changing or removing feature flags. The capability behind the flag is its own ✨ feat commit. |
| ⚗️ | `:alembic:` | chore | — | Experiments and spikes that are expected to be revisited. |
| 💸 | `:money_with_wings:` | chore | — | Sponsorships, billing or money-related infrastructure. |
| 🥚 | `:egg:` | chore | — | Easter eggs. |
| 📄 | `:page_facing_up:` | chore | `docs` if the commit only explains the license in documentation | Adding or changing the license. |
| 🔀 | `:twisted_rightwards_arrows:` | chore | — | Merge commits. Prefer the default message git generates; only write one by hand when the merge needs explanation. |

## revert

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| ⏪️ | `:rewind:` | revert | — | Reverting a previous commit. The body names the reverted commit and why. **default revert** |

## Modifier

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 💥 | `:boom:` | any | — | Breaking change: consumers must change something. It replaces the type's gitmoji, keeps the type, and always carries `!` after the scope plus a `BREAKING CHANGE:` footer. `💥 feat(api)!: …` |

## Never in shared history

| Gitmoji | Code | Type | Exception | Use for |
|---|---|---|---|---|
| 🚧 | `:construction:` | chore | — | ⚠ Work in progress. Only on a personal branch that will be squashed. |
| 💩 | `:poop:` | refactor | — | ⚠ Knowingly bad code to improve later. Prefer a TODO with a ticket. |
| 🍻 | `:beers:` | chore | — | ⚠ Joke gitmoji. Never in a professional repository. |
