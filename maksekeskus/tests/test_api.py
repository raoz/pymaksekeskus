import unittest
import maksekeskus.api as api
from maksekeskus.models import Customer, Transaction
from decimal import *


class TestMaksekeskusAPI(unittest.TestCase):

    def setUp(self):
        self.api = api.MaksekeskusAPI(
            False,
            "f7741ab2-7445-45f9-9af4-0d0408ef1e4c",
            "pfOsGD9oPaFEILwqFLHEHkPf7vZz4j3t36nAcufP1abqT9l99koyuC1IWAOcBeqt",
            "zPA6jCTIvGKYqrXxlgkXLzv3F82Mjv2E"
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

