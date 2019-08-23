import unittest
import maksekeskus.api as api
from maksekeskus.models import Customer, Transaction


class TestMaksekeskusAPI(unittest.TestCase):

    def setUp(self):
        self.api = api.MaksekeskusAPI(
            True,
            "1ca58c6f-89c2-442f-950a-cd5fa3484397",
            "4amoXJ9cGuoD4zoQDdmCSCbGb3he2ef2IbazM4nUOMjSPQEABave8vnoc6I7sNf9",
            "3TT6Jlm5YWvsdT0p5w5bqRuhnr9F5FIYpsVYE8UsVfKYZBeUXaVdRgl4ykAuQ8j5"
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
                reference="pymaksekeskus test fee"
            )
        )

    def test_create_transaction(self):
        amount = 13.37
        transaction = self.create_transaction(amount)
        self.assertIn("_links", transaction)
        self.assertIn("payment_methods", transaction)
        self.assertEqual(amount, transaction["amount"])

    def test_create_and_get_transaction(self):
        amount = 13.37
        transaction = self.create_transaction(amount)
        print(transaction['id'])
        transaction = self.api.get_transaction(transaction['id'])
        self.assertEqual(amount, transaction["amount"])
        self.assertEqual("pymaksekeskus test fee", transaction["reference"])

