import unittest

from ibkr_dashboard import Quote, configured_watchlist, suggestion_for_quote


class SuggestionTests(unittest.TestCase):
    def test_watch_for_buy_when_price_is_two_percent_below_close(self):
        result = suggestion_for_quote(Quote("AAPL", 98.0, 100.0))

        self.assertEqual(result["suggestion"], "WATCH FOR BUY")
        self.assertEqual(result["change_percent"], -2.0)

    def test_hold_when_price_is_within_thresholds(self):
        result = suggestion_for_quote(Quote("AAPL", 101.0, 100.0))

        self.assertEqual(result["suggestion"], "HOLD / MONITOR")

    def test_unavailable_without_usable_market_data(self):
        result = suggestion_for_quote(Quote("AAPL", None, 100.0))

        self.assertEqual(result["suggestion"], "UNAVAILABLE")

    def test_watchlist_is_deduplicated_and_normalized(self):
        self.assertEqual(configured_watchlist("aapl, MSFT, AAPL"), ("AAPL", "MSFT"))


if __name__ == "__main__":
    unittest.main()
