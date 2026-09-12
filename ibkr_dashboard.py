"""Local, read-only IBKR market-data dashboard.

This module never submits, modifies, or cancels an order.
"""

import math
import os
import re
from dataclasses import asdict, dataclass
from typing import Iterable, Optional

from flask import Flask, jsonify, render_template_string
from ib_insync import IB, Stock


DEFAULT_WATCHLIST = ("AAPL", "MSFT", "NVDA", "SPY")
SYMBOL_PATTERN = re.compile(r"^[A-Z][A-Z0-9.-]{0,14}$")
BUY_THRESHOLD_PERCENT = -2.0
SELL_THRESHOLD_PERCENT = 2.0

app = Flask(__name__)


@dataclass(frozen=True)
class Quote:
    symbol: str
    price: Optional[float]
    previous_close: Optional[float]


def configured_watchlist(value: Optional[str] = None) -> tuple[str, ...]:
    raw_symbols = (value if value is not None else os.getenv("IBKR_WATCHLIST", "")).split(",")
    symbols = tuple(symbol.strip().upper() for symbol in raw_symbols if symbol.strip())
    if not symbols:
        return DEFAULT_WATCHLIST
    invalid_symbols = [symbol for symbol in symbols if not SYMBOL_PATTERN.fullmatch(symbol)]
    if invalid_symbols:
        raise ValueError(f"Invalid IBKR_WATCHLIST symbol(s): {', '.join(invalid_symbols)}")
    return tuple(dict.fromkeys(symbols))


def finite_price(value: object) -> Optional[float]:
    if isinstance(value, (int, float)) and math.isfinite(value) and value > 0:
        return float(value)
    return None


def suggestion_for_quote(quote: Quote) -> dict:
    result = asdict(quote)
    price = quote.price
    previous_close = quote.previous_close
    if price is None or previous_close is None:
        return {
            **result,
            "change_percent": None,
            "suggestion": "UNAVAILABLE",
            "reason": "IBKR did not return both a current price and previous close.",
        }

    change_percent = (price - previous_close) / previous_close * 100
    if change_percent <= BUY_THRESHOLD_PERCENT:
        suggestion = "WATCH FOR BUY"
        reason = f"Price is {abs(change_percent):.2f}% below the previous close."
    elif change_percent >= SELL_THRESHOLD_PERCENT:
        suggestion = "WATCH FOR SELL"
        reason = f"Price is {change_percent:.2f}% above the previous close."
    else:
        suggestion = "HOLD / MONITOR"
        reason = f"Price is {change_percent:.2f}% from the previous close."
    return {**result, "change_percent": round(change_percent, 2), "suggestion": suggestion, "reason": reason}


class IbkrMarketDataClient:
    """Requests snapshot prices from an already authenticated TWS or IB Gateway session."""

    def __init__(self, host: str, port: int, client_id: int) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id

    def fetch_quotes(self, symbols: Iterable[str]) -> list[Quote]:
        ib = IB()
        try:
            ib.connect(self.host, self.port, clientId=self.client_id, timeout=5, readonly=True)
            contracts = [Stock(symbol, "SMART", "USD") for symbol in symbols]
            ib.qualifyContracts(*contracts)
            tickers = ib.reqTickers(*contracts)
            return [
                Quote(
                    symbol=ticker.contract.symbol,
                    price=finite_price(ticker.marketPrice())
                    or finite_price(ticker.last)
                    or finite_price(ticker.close),
                    previous_close=finite_price(ticker.close),
                )
                for ticker in tickers
            ]
        finally:
            if ib.isConnected():
                ib.disconnect()


def market_data_client() -> IbkrMarketDataClient:
    return IbkrMarketDataClient(
        host=os.getenv("IBKR_HOST", "127.0.0.1"),
        port=int(os.getenv("IBKR_PORT", "7496")),
        client_id=int(os.getenv("IBKR_CLIENT_ID", "21")),
    )


@app.get("/")
def dashboard():
    return render_template_string(PAGE_TEMPLATE)


@app.get("/api/suggestions")
def suggestions():
    try:
        quotes = market_data_client().fetch_quotes(configured_watchlist())
    except (ConnectionError, OSError, RuntimeError, TimeoutError, ValueError) as error:
        return jsonify(
            {
                "error": (
                    "Could not read IBKR market data. Confirm TWS or IB Gateway is running, "
                    "API connections are enabled, and the configured port is correct. "
                    f"Details: {error}"
                )
            }
        ), 503
    return jsonify({"quotes": [suggestion_for_quote(quote) for quote in quotes]})


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IBKR Market Suggestions</title>
  <style>
    body { background: #101827; color: #e5e7eb; font: 16px system-ui, sans-serif; margin: 0; }
    main { margin: 3rem auto; max-width: 960px; padding: 0 1.5rem; }
    h1 { margin-bottom: .25rem; } .notice { color: #fbbf24; }
    button { background: #2563eb; border: 0; border-radius: .4rem; color: white; cursor: pointer; padding: .7rem 1rem; }
    table { background: #1f2937; border-collapse: collapse; margin-top: 1.5rem; width: 100%; }
    td, th { border-bottom: 1px solid #374151; padding: .8rem; text-align: left; }
    .error { background: #7f1d1d; border-radius: .4rem; margin-top: 1rem; padding: 1rem; }
  </style>
</head>
<body>
  <main>
    <h1>IBKR Market Suggestions</h1>
    <p class="notice"><strong>Read-only:</strong> this dashboard cannot submit orders. Suggestions are simple price-change indicators, not financial advice.</p>
    <button id="refresh">Refresh market data</button>
    <div id="status" aria-live="polite"></div>
    <table>
      <thead><tr><th>Symbol</th><th>Price</th><th>Previous close</th><th>Change</th><th>Suggestion</th><th>Reason</th></tr></thead>
      <tbody id="quotes"></tbody>
    </table>
  </main>
  <script>
    const formatPrice = value => value === null ? "Unavailable" : `$${value.toFixed(2)}`;
    const formatChange = value => value === null ? "Unavailable" : `${value.toFixed(2)}%`;
    async function refresh() {
      const status = document.getElementById("status");
      status.textContent = "Loading market data...";
      status.className = "";
      const response = await fetch("/api/suggestions");
      const data = await response.json();
      if (!response.ok) {
        status.textContent = data.error;
        status.className = "error";
        return;
      }
      document.getElementById("quotes").innerHTML = data.quotes.map(quote => `
        <tr><td>${quote.symbol}</td><td>${formatPrice(quote.price)}</td><td>${formatPrice(quote.previous_close)}</td>
        <td>${formatChange(quote.change_percent)}</td><td>${quote.suggestion}</td><td>${quote.reason}</td></tr>
      `).join("");
      status.textContent = `Updated ${new Date().toLocaleTimeString()}.`;
    }
    document.getElementById("refresh").addEventListener("click", refresh);
    refresh();
  </script>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
