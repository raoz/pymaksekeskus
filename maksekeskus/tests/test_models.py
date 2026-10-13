"""Offline unit tests: no network access or credentials required."""
import unittest
from decimal import Decimal
from unittest import mock

from maksekeskus.api import MaksekeskusAPI
from maksekeskus.errors import MaksekeskusError
from maksekeskus.models import Customer, Transaction


class TestModels(unittest.TestCase):

    def test_customer_dict_drops_none(self):
        self.assertEqual({"ip": "1.2.3.4", "country": "ee"}, Customer(ip="1.2.3.4", country="ee").dict())

    def test_customer_requires_ip(self):
        with self.assertRaises(ValueError):
            Customer(ip=None).dict()

    def test_transaction_dict_with_callback_urls(self):
        url = {"method": "POST", "url": "https://example.com"}
        data = Transaction(amount=Decimal("1.23"), currency="EUR", reference="ref",
                           cancel_url=url, notification_url=url, return_url=url).dict()
        self.assertEqual(Decimal("1.23"), data["amount"])
        self.assertEqual(url, data["transaction_url"]["return_url"])

    def test_transaction_requires_all_or_no_callback_urls(self):
        with self.assertRaises(ValueError):
            Transaction(amount=1, currency="EUR", return_url={"url": "x"}).dict()


class TestRequest(unittest.TestCase):

    def make_api(self, ok=True, text="{}"):
        session = mock.Mock()
        session.request.return_value = mock.Mock(ok=ok, text=text)
        return MaksekeskusAPI(False, "shop", "secret", "publishable", session=session), session

    def test_uses_test_environment_and_secret_key(self):
        api, session = self.make_api(text='{"amount": 13.37}')
        result = api.get_transaction("abc")
        args, kwargs = session.request.call_args
        self.assertEqual(("GET", "https://api.test.maksekeskus.ee/v1/transactions/abc"), args)
        self.assertEqual("secret", kwargs["auth"].password)
        self.assertEqual(Decimal("13.37"), result["amount"])

    def test_error_response_raises(self):
        api, _ = self.make_api(ok=False, text="error")
        with self.assertRaises(MaksekeskusError):
            api.get_transactions()


if __name__ == "__main__":
    unittest.main()
