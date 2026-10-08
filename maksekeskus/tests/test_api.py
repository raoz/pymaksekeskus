import os
import unittest
import maksekeskus.api as api
from maksekeskus.models import Customer, Transaction
from decimal import *

CREDENTIAL_VARS = ("MAKSEKESKUS_SHOP_ID", "MAKSEKESKUS_SECRET_KEY", "MAKSEKESKUS_PUBLISHABLE_KEY")
MISSING_CREDENTIALS = [name for name in CREDENTIAL_VARS if not os.environ.get(name)]


@unittest.skipIf(MISSING_CREDENTIALS, "Maksekeskus test-environment credentials not set: " + ", ".join(MISSING_CREDENTIALS))
class TestMaksekeskusAPI(unittest.TestCase):

    def setUp(self):
        self.api = api.MaksekeskusAPI(
            False,
            os.environ["MAKSEKESKUS_SHOP_ID"],
            os.environ["MAKSEKESKUS_SECRET_KEY"],
            os.environ["MAKSEKESKUS_PUBLISHABLE_KEY"],
        )

    def tearDown(self):
        self.api.close()

    def test_get_shop_configuration(self):
        config = self.api.get_config("pymaksekeskus_test")
        self.assertIn("payment_methods", config)

    def test_get_transactions(self):
        transactions = self.api.get_transactions()
        self.assertTrue(isinstance(transactions, list))

    def create_transaction(self, amount):
        return self.api.create_transaction(
            Customer(
                country="ee",
                email="pymaksekeskus@codeduf.eu",
                ip="1.2.3.4",
                locale="et"
            ),
            Transaction(
                amount=amount,
                currency="EUR",
                reference="pymaksekeskus test fee",
                return_url = {
                    'method': 'POST',
                    'url': "https://codeduf.eu"
                    },
                notification_url = {
                    'method': 'POST',
                    'url': "https://codeduf.eu"
                    },
                cancel_url = {
                    'method': 'POST',
                    'url': "https://codeduf.eu"
                    },
            )
        )

    def test_create_transaction(self):
        amount = 13
        transaction = self.create_transaction(amount)
        print(transaction)
        self.assertIn("_links", transaction)
        self.assertIn("payment_methods", transaction)
        self.assertEqual(13, transaction["amount"])

    def test_create_transaction_decimal(self):
        amount = Decimal("13.37")
        transaction = self.create_transaction(amount)
        self.assertIn("_links", transaction)
        self.assertIn("payment_methods", transaction)
        self.assertTrue(amount, transaction["amount"])

    def test_create_and_get_transaction(self):
        amount = Decimal("13.37")
        transaction = self.create_transaction(amount)
        print(transaction['id'])
        transaction = self.api.get_transaction(transaction['id'])
        self.assertEqual(amount, transaction["amount"])
        self.assertEqual("pymaksekeskus test fee", transaction["reference"])

