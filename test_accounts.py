
import unittest
from unittest.mock import patch

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account('test_user')

    def test_initial_state(self):
        self.assertEqual(self.account.user_id, 'test_user')
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])

    def test_deposit_funds(self):
        self.account.deposit_funds(100.0)
        self.assertEqual(self.account.balance, 100.0)

    def test_deposit_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-50.0)

    def test_withdraw_funds(self):
        self.account.deposit_funds(100.0)
        self.account.withdraw_funds(50.0)
        self.assertEqual(self.account.balance, 50.0)

    def test_withdraw_exceeding_balance(self):
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(50.0)

    def test_withdraw_negative_amount(self):
        with self.assertRaises(ValueError):
            self.account.withdraw_funds(-50.0)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_buy_shares(self, mock_get_share_price):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.balance, 150.0)
        self.assertEqual(self.account.holdings['AAPL'], 1)
        self.assertEqual(len(self.account.transactions), 1)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_buy_shares_insufficient_balance(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.buy_shares('AAPL', 1)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_shares(self, mock_get_share_price):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.balance, 300.0)
        self.assertEqual(self.account.holdings.get('AAPL', 0), 0)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_sell_shares_insufficient_holdings(self, mock_get_share_price):
        with self.assertRaises(ValueError):
            self.account.sell_shares('AAPL', 1)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_portfolio_value(self, mock_get_share_price):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        self.assertEqual(self.account.portfolio_value(), 300.0)

    @patch('__main__.get_share_price', return_value=150.0)
    def test_profit_or_loss(self, mock_get_share_price):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        self.account.sell_shares('AAPL', 1)
        self.assertEqual(self.account.profit_or_loss(), 0.0)

    def test_report_holdings(self):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        holdings = self.account.report_holdings()
        self.assertEqual(holdings, {'AAPL': 1})

    def test_transaction_history(self):
        self.account.deposit_funds(300.0)
        self.account.buy_shares('AAPL', 1)
        transactions = self.account.transaction_history()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0][:2], ('buy', 'AAPL'))

if __name__ == '__main__':
    unittest.main()
