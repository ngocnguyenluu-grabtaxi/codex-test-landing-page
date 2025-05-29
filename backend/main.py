from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
import pathlib
import requests

# In-memory watchlist storage
watchlist = set()

# Simple currency conversion rates relative to USD
RATES = {
    "USD": 1.0,
    "EUR": 0.9,
    "JPY": 110.0,
    "SGD": 1.35,
}


def update_rates():
    """Fetch live currency rates relative to USD and update RATES."""
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        rates = data.get("rates", {})
        for cur in list(RATES.keys()):
            if cur in rates:
                RATES[cur] = rates[cur]
    except Exception:
        # On network failure keep existing rates
        pass

app = FastAPI()

# Path to the frontend build directory
frontend_build = pathlib.Path(__file__).resolve().parents[1] / "frontend" / "build"

app.mount("/", StaticFiles(directory=frontend_build, html=True), name="static")


def fetch_price(symbol: str) -> dict:
    """Fetch latest stock price from Yahoo Finance."""
    url = (
        "https://query1.finance.yahoo.com/v7/finance/quote"
        f"?symbols={symbol}"
    )
    response = requests.get(url, timeout=5)
    data = response.json()
    result = data["quoteResponse"]["result"][0]
    return {
        "price": result["regularMarketPrice"],
        "currency": result["currency"],
    }


def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount between currencies. Fetch live rates if possible."""
    update_rates()
    if from_currency not in RATES or to_currency not in RATES:
        raise HTTPException(status_code=400, detail="Unsupported currency")
    usd = amount / RATES[from_currency]
    return usd * RATES[to_currency]


@app.post("/api/watchlist")
def add_stock(symbol: str):
    symbol = symbol.upper()
    if symbol in watchlist:
        raise HTTPException(status_code=400, detail="Already in watchlist")
    watchlist.add(symbol)
    return {"watchlist": sorted(watchlist)}


@app.get("/api/watchlist")
def get_watchlist(search: str = Query("", alias="search")):
    search = search.upper()
    if search:
        results = [s for s in watchlist if search in s]
    else:
        results = list(watchlist)
    return {"watchlist": sorted(results)}


@app.delete("/api/watchlist/{symbol}")
def remove_stock(symbol: str):
    symbol = symbol.upper()
    if symbol not in watchlist:
        raise HTTPException(status_code=404, detail="Not in watchlist")
    watchlist.remove(symbol)
    return {"watchlist": sorted(watchlist)}


@app.get("/api/price/{symbol}")
def price(symbol: str, currency: str = "USD"):
    data = fetch_price(symbol)
    converted = convert_currency(data["price"], data["currency"], currency)
    return {"symbol": symbol.upper(), "price": converted, "currency": currency}
