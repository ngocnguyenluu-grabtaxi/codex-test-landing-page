# Stocks Monitoring App Specification

## Overview
The application provides a simple way to monitor stock prices. Users can
maintain a watchlist of stock symbols, fetch the latest prices from Yahoo
Finance and view prices in different currencies.

The project consists of a React frontend and a FastAPI backend.

## Backend API
- `POST /api/watchlist?symbol=SYMBOL` – Add a stock symbol to the watchlist.
- `GET /api/watchlist?search=TERM` – Retrieve the watchlist; optional `search`
  parameter filters symbols containing `TERM`.
- `DELETE /api/watchlist/{symbol}` – Remove a symbol from the watchlist.
- `GET /api/price/{symbol}?currency=CUR` – Get the latest price for `symbol`
  converted to the desired currency (`USD`, `EUR`, `JPY` or `SGD`).

Prices are fetched from Yahoo Finance. Currency conversion first attempts to
retrieve live exchange rates from `open.er-api.com` and falls back to built-in
rates when the request fails.

## Frontend
- Displays the list of watchlist symbols with their latest prices.
- Allows searching within the watchlist.
- Provides a form to add new symbols and a button to remove existing ones.
 - Prices can be displayed in USD, EUR, JPY or SGD using a currency selector.

## Running
See `backend/AGENTS.md` and `frontend/AGENTS.md` for setup instructions.
