# Offline Operations Evidence Tracer

**Status:** prototype — core flow works, still in development.

Offline Operations Evidence Tracer is a local web app for exploring synthetic order, stock, invoice, and payment records as one clickable evidence trail. It is intended to make broken links, conflicting quantities, and unexplained status changes easy to spot and explain.

Built by a supervised autonomous agent pipeline (nightshift).

## Run

Requires Python 3.10 or later. From this directory:

```text
python app.py
```

Then open `http://127.0.0.1:8000` in a browser. The current view is a skeleton; the clickable trail and rules arrive in later milestones.

## Synthetic evidence store

`evidence_store.py` provides a repeatable local SQLite schema and seed data for three synthetic transactions. It records linked stock movements, invoices, and payments, including a quantity-conflict scenario and an intentionally missing payment link for the upcoming rules API. Call `seed_database()` to create a local demo database; generated databases are not stored in the repository.

## Test

```text
python -m unittest discover -s tests
```

All sample data is synthetic. The app makes no network requests at runtime.

## License

MIT — see [LICENSE](LICENSE).
