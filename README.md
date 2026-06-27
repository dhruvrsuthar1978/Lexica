# Text to SQL App

This workspace is split into separate frontend and backend projects.

## Backend

```bash
cd backend
python -m pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Backend runs at `http://127.0.0.1:8000`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at the Vite URL, usually `http://127.0.0.1:5173`.

During local development, Vite proxies `/api/*` and `/health` to the FastAPI backend. For a deployed frontend, set `VITE_API_BASE_URL` to the backend origin.
