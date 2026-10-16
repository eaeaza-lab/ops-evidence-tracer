# Execution Plan

## Milestones

- [x] **M0 setup** — **stage: mvp**. Establish specification, repository rules, offline runner configuration, and a tested server skeleton. Acceptance: `python -m unittest discover -s tests`
- [ ] **M1 synthetic evidence store** — **stage: mvp**. Add SQLite schema, repeatable synthetic seed records, and evidence-link queries. Acceptance: `python -m unittest discover -s tests`
- [ ] **M2 evidence rules API** — **stage: mvp**. Implement missing-link, quantity-conflict, and status-transition checks as JSON endpoints. Acceptance: `python -m unittest discover -s tests`
- [ ] **M3 clickable trail UI** — **stage: mvp**. Build the local HTML/CSS/JavaScript transaction list and evidence trail view. Acceptance: `python -m unittest discover -s tests`
- [ ] **M4 showcase polish** — **stage: polish**. Improve empty/error states, visual hierarchy, and demonstration guidance. Acceptance: `python -m unittest discover -s tests`
- [ ] **M5 release verification** — **stage: polish**. Add end-to-end smoke coverage and verify documentation against the implementation. Acceptance: `python -m unittest discover -s tests`

## Progress log

- 2026-10-16: M0 completed. Created the project contract, an offline server/UI skeleton, and passing standard-library tests.

## Decision log

- 2026-10-16: Use only Python's standard library, SQLite, and local browser assets to keep the project offline and easy to run.
- 2026-10-16: Start with a server skeleton before defining persistent schema details in M1.

