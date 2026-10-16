# Future-session guide

## Commands

- Run tests: `python -m unittest discover -s tests`
- Run the local app: `python app.py`

## Rules

- Keep all business data synthetic; never add real company, person, marketplace, or account names.
- Use Python standard library, SQLite, and local HTML/CSS/JavaScript unless the user explicitly changes the stack.
- The application must not make network requests at runtime.
- Add or update tests with behavior changes, and run the test command before handoff.
- Keep `.nightshift.json` commands Windows-compatible, offline, and within the runner's allowed command prefixes. Put multi-step checks inside Python scripts, never shell wrappers.
- Do not add secrets, commit generated databases, or hand-write lockfiles/checksums.

