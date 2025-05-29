import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from fastapi.testclient import TestClient
import pytest

from main import app, watchlist, fetch_price, RATES

client = TestClient(app)


def setup_function():
    watchlist.clear()


def test_add_and_remove_stock():
    response = client.post("/api/watchlist", params={"symbol": "AAPL"})
    assert response.status_code == 200
    assert response.json() == {"watchlist": ["AAPL"]}

    response = client.delete("/api/watchlist/AAPL")
    assert response.status_code == 200
    assert response.json() == {"watchlist": []}


def test_search_watchlist():
    client.post("/api/watchlist", params={"symbol": "AAPL"})
    client.post("/api/watchlist", params={"symbol": "MSFT"})
    res = client.get("/api/watchlist", params={"search": "AA"})
    assert res.json() == {"watchlist": ["AAPL"]}


def test_price_endpoint(monkeypatch):
    def fake_fetch_price(symbol):
        return {"price": 100, "currency": "USD"}

    def fake_get(url, timeout=5):
        return type("Resp", (), {"json": lambda self: {"rates": {"USD": 1.0, "EUR": 0.9, "JPY": 110.0, "SGD": 1.3}}})()

    monkeypatch.setattr("main.fetch_price", fake_fetch_price)
    monkeypatch.setattr("main.requests.get", fake_get)

    res = client.get("/api/price/AAPL", params={"currency": "EUR"})
    assert res.status_code == 200
    data = res.json()
    assert data["symbol"] == "AAPL"
    # Conversion USD->EUR uses rate 0.9
    assert data["price"] == pytest.approx(90)
    assert data["currency"] == "EUR"


def test_update_rates(monkeypatch):
    def fake_get(url, timeout=5):
        return type("Resp", (), {"json": lambda self: {"rates": {"USD": 1.0, "EUR": 0.8, "JPY": 105.0, "SGD": 1.2}}})()
    monkeypatch.setattr("main.requests.get", fake_get)
    from main import update_rates
    update_rates()
    assert RATES["EUR"] == 0.8
    assert RATES["SGD"] == 1.2
