# Backend instructions

- This folder contains a FastAPI application that manages a stock watchlist.
- Install dependencies listed in `requirements.txt` using `pip install -r requirements.txt`.
- The repo includes lightweight `fastapi` and `requests` stubs so tests run without network access.
- Currency conversion attempts to fetch live rates from `open.er-api.com` but falls back to static values if the request fails.
- Run the server with `uvicorn main:app --reload` from this directory.
- Static files are served from `../frontend/build`.
- Run backend unit tests with `pytest`.
