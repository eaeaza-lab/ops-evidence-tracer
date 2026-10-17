import sqlite3
import unittest

import evidence_store


class EvidenceStoreTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.row_factory = sqlite3.Row
        evidence_store.initialize(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_seed_contains_linked_synthetic_evidence(self):
        transactions = evidence_store.list_transactions(self.connection)
        self.assertEqual([item["reference"] for item in transactions], ["TXN-1001", "TXN-1002", "TXN-1003"])
        evidence = evidence_store.get_evidence_links(self.connection, "txn-clear")
        self.assertEqual([item["evidence_type"] for item in evidence], ["stock_movement", "invoice", "payment"])

    def test_seed_is_repeatable_without_duplicate_records(self):
        evidence_store.initialize(self.connection)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0], 3)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM stock_movements").fetchone()[0], 3)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM invoices").fetchone()[0], 3)
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM payments").fetchone()[0], 2)

    def test_missing_payment_scenario_has_no_payment_link(self):
        evidence = evidence_store.get_evidence_links(self.connection, "txn-missing-payment")
        self.assertEqual([item["evidence_type"] for item in evidence], ["stock_movement", "invoice"])

    def test_quantity_conflict_scenario_preserves_both_source_quantities(self):
        evidence = evidence_store.get_evidence_links(self.connection, "txn-quantity")
        quantities = {item["evidence_type"]: item["quantity"] for item in evidence}
        self.assertEqual(quantities["stock_movement"], 8)
        self.assertEqual(quantities["invoice"], 10)


if __name__ == "__main__":
    unittest.main()
