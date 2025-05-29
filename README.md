# Test Landing Page

This repository contains a React frontend and a FastAPI backend implementing a
simple stocks monitoring application.

- `frontend/` holds a small React application that can be built into static files.
- `backend/` hosts a FastAPI app that serves the built frontend files.

Refer to the `AGENTS.md` files in each folder for setup instructions and
`SPEC.md` for details about the application. The backend uses lightweight stub
implementations of `fastapi` and `requests` so that tests can run offline.
