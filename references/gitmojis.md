# Gitmoji catalog

All 75 gitmojis, sorted by main type.
**Types** = commit types the gitmoji may be used with (first = main). Any pair not listed here is invalid.
`⚡️` and `⚡` (with or without the variation selector) are the same gitmoji.

| Gitmoji | Code | Types | Use for |
|---|---|---|---|
| ✨ | `:sparkles:` | feat | A capability that did not exist before: new screen, endpoint, option, command, integration. **default feat** |
| 💄 | `:lipstick:` | feat, fix | A change whose essence is visual: styles, themes, layout, spacing, colors. Use feat for new visuals, fix for broken ones. |
| 🚧 | `:construction:` | feat, fix, refactor | ⚠ Work in progress. Only on personal branches that will be squashed. |
| 📈 | `:chart_with_upwards_trend:` | feat, fix | Analytics, tracking events, metrics instrumentation. |
| 🌐 | `:globe_with_meridians:` | feat, fix | Translations, locales, date/number formatting per locale. |
| 💩 | `:poop:` | feat, fix, refactor | ⚠ Knowingly bad code to improve later. Avoid in shared history; prefer a TODO with a ticket. |
| 💥 | `:boom:` | feat, fix, refactor, perf, build | Breaking change: consumers must change something. Always paired with `!` after the scope and a BREAKING CHANGE footer. |
| 🍱 | `:bento:` | feat, fix, chore | Static assets: images, icons, fonts, media. |
| ♿️ | `:wheelchair:` | feat, fix | Accessibility: keyboard navigation, ARIA, contrast, screen-reader support. |
| 💬 | `:speech_balloon:` | feat, fix | User-facing text, copy, messages, literals. |
| 🗃️ | `:card_file_box:` | feat, fix, refactor, perf | Database changes: schema, migrations, indexes, queries whose essence is the data layer. |
| 🔊 | `:loud_sound:` | feat, chore | Adding or improving logs. |
| 🚸 | `:children_crossing:` | feat, fix | Usability: fewer steps, clearer flows, better feedback to the user. |
| 📱 | `:iphone:` | feat, fix | Responsive design and mobile layouts. |
| 🥚 | `:egg:` | feat | Easter eggs. |
| ⚗️ | `:alembic:` | feat, chore | Experiments and spikes that are expected to be revisited. |
| 🔍️ | `:mag:` | feat, fix | SEO: meta tags, sitemaps, structured data, indexability. |
| 🏷️ | `:label:` | feat, fix, refactor | Type definitions and typings (TypeScript types, interfaces, schemas for types). |
| 🚩 | `:triangular_flag_on_post:` | feat, chore | Adding, changing or removing feature flags. |
| 💫 | `:dizzy:` | feat, fix | Animations and transitions. |
| 🛂 | `:passport_control:` | feat, fix | Authorization, roles and permissions. |
| 👔 | `:necktie:` | feat, fix | Business rules and domain logic: calculations, policies, workflows of the domain. |
| 🩺 | `:stethoscope:` | feat, fix | Healthchecks and readiness/liveness probes. |
| 💸 | `:money_with_wings:` | feat, chore | Sponsorships, billing or money-related infrastructure. |
| 🧵 | `:thread:` | feat, fix, perf, refactor | Concurrency, multithreading, async coordination, locks, queues. |
| 🦺 | `:safety_vest:` | feat, fix | Input validation and data validation rules. |
| ✈️ | `:airplane:` | feat, fix | Offline support, caching for offline use, sync on reconnect. |
| 🦖 | `:t-rex:` | feat, fix, refactor | Backwards compatibility: shims, polyfills, keeping old clients working. |
| 🐛 | `:bug:` | fix | A behavior that was supposed to work and did not: wrong result, crash, broken flow. **default fix** |
| 🚑️ | `:ambulance:` | fix | Urgent fix shipped straight to production (hotfix) because something critical is down or losing data. |
| 🔒️ | `:lock:` | fix | Closing a security or privacy hole: injection, leaked data, missing auth check, unsafe defaults. |
| 🚨 | `:rotating_light:` | fix, style | Silencing compiler or linter warnings. style if it is purely cosmetic, fix if the warning pointed at a real problem. |
| ✏️ | `:pencil2:` | fix, docs | Typos. docs for typos in documentation, fix for typos users see or that break code. |
| 👽️ | `:alien:` | fix, refactor | Adapting to a change in an external API or third-party service. |
| 🥅 | `:goal_net:` | fix, feat | Catching and handling errors that previously escaped. |
| 🩹 | `:adhesive_bandage:` | fix | Small, non-critical fix: an edge case, a minor glitch. |
| ♻️ | `:recycle:` | refactor | Restructuring code without changing what it does: extract, rename, simplify, reorganize. **default refactor** |
| 🔥 | `:fire:` | refactor, chore | Removing code or files that are no longer needed. Removing a public capability is a breaking change: use 💥 instead. |
| 🚚 | `:truck:` | refactor, chore | Moving or renaming files, folders, routes or modules. |
| 🏗️ | `:building_construction:` | refactor | Architectural changes: layers, boundaries, module structure, patterns across the codebase. |
| 🗑️ | `:wastebasket:` | refactor, chore | Deprecating code that will be removed later (marking, warnings, migration notes). |
| ⚰️ | `:coffin:` | refactor, chore | Removing dead code that nothing references. |
| ⚡️ | `:zap:` | perf | Measurably faster or lighter code with the same observable result. **default perf** |
| 🎨 | `:art:` | style | Formatting or code-structure changes with zero behavior change: whitespace, import order, lint autofix, prettier run. Never for CSS/UI. **default style** |
| 📝 | `:memo:` | docs | README, guides, ADRs, API docs, changelog prose written by hand. **default docs** |
| 💡 | `:bulb:` | docs | Comments inside source code (docblocks, explanatory comments). |
| 👥 | `:busts_in_silhouette:` | docs, chore | Contributors lists, CODEOWNERS, maintainers. |
| ✅ | `:white_check_mark:` | test | Adding, updating or fixing tests without touching production code. **default test** |
| 🤡 | `:clown_face:` | test | Mocks, stubs, fakes and fixtures for tests. |
| 📸 | `:camera_flash:` | test | Snapshot files for tests. |
| 🧪 | `:test_tube:` | test | Adding a failing test on purpose (reproducing a bug before fixing it, TDD red step). |
| 📦️ | `:package:` | build | Build system, packaging, compiled artifacts, Dockerfiles, bundler output. **default build** |
| ⬇️ | `:arrow_down:` | build | Downgrading one or more dependencies. |
| ⬆️ | `:arrow_up:` | build | Upgrading one or more dependencies. |
| 📌 | `:pushpin:` | build | Pinning dependencies to exact versions. |
| ➕ | `:heavy_plus_sign:` | build | Adding a dependency on its own. If the dependency exists only to implement a feature, it belongs to that feat commit. |
| ➖ | `:heavy_minus_sign:` | build | Removing a dependency. |
| 🧱 | `:bricks:` | build, ci, chore | Infrastructure: IaC, containers orchestration, cloud resources, networking. |
| 👷 | `:construction_worker:` | ci | Adding or changing CI configuration: workflows, jobs, runners, caches. **default ci** |
| 🚀 | `:rocket:` | ci, chore | Deployment configuration or deploy-only changes (pipelines, platform manifests, release scripts). |
| 💚 | `:green_heart:` | ci | Repairing a broken CI pipeline. |
| 🔧 | `:wrench:` | chore, build | Configuration files: linters, editors, tsconfig, bundler, environment defaults. **default chore** |
| 🎉 | `:tada:` | chore | The very first commit of a project. Only once per repository. |
| 🔐 | `:closed_lock_with_key:` | chore, ci | Encrypted secrets, secret templates (.env.example) or secret-manager wiring. Never commit a real secret. |
| 🔖 | `:bookmark:` | chore | Release commits: version bump, release notes, tags (chore(release)). |
| 🔨 | `:hammer:` | chore, build | Development scripts: Makefile targets, npm scripts, local tooling. |
| 🔀 | `:twisted_rightwards_arrows:` | chore | Merge commits. Prefer the default message git generates; only write one by hand when the merge needs explanation. |
| 📄 | `:page_facing_up:` | chore, docs | Adding or changing the license. |
| 🍻 | `:beers:` | chore | ⚠ Joke gitmoji. Never in a professional repository. |
| 🔇 | `:mute:` | chore, refactor | Removing logs. |
| 🙈 | `:see_no_evil:` | chore | Changes to .gitignore (or other ignore files). |
| 🌱 | `:seedling:` | chore, feat | Seed data for databases or local environments. |
| 🧐 | `:monocle_face:` | chore | Data exploration and inspection (notebooks, queries, analysis scripts). |
| 🧑‍💻 | `:technologist:` | chore, build | Developer experience: faster local setup, better tooling, dev containers. |
| ⏪️ | `:rewind:` | revert | Reverting a previous commit. The body names the reverted commit and why. **default revert** |

Breaking change with any type: `💥 type(scope)!: title` + footer `BREAKING CHANGE: <what consumers must change>`.
