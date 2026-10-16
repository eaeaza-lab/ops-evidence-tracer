# Offline Operations Evidence Tracer

Status: **work in progress**

Offline Operations Evidence Tracer is a local web app for exploring synthetic order, stock, invoice, and payment records as one clickable evidence trail. It is intended to make broken links, conflicting quantities, and unexplained status changes easy to spot and explain.

Built by a supervised autonomous agent pipeline (nightshift).

## Run

Requires Python 3.10 or later. From this directory:

```text
python app.py
```

Then open `http://127.0.0.1:8000` in a browser. The current view is a skeleton; evidence storage and rules arrive in the next milestones.

## Test

```text
python -m unittest discover -s tests
```

All sample data is synthetic. The app makes no network requests at runtime.

