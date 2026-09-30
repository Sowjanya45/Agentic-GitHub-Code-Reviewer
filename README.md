# CodeLens — Agentic GitHub Code Reviewer

AI-powered GitHub pull-request reviewer built on LangGraph agents, Tree-sitter, Semgrep and pgvector.
See the roadmap below; **this repo is currently at Phase 1 (backend foundation).**

## Status

| Phase | Scope | State |
|---|---|---|
| 1 | FastAPI, PostgreSQL, SQLAlchemy, Alembic, `/health`, config, logging, Docker | done |
| 2+ | GitHub OAuth, PR retrieval, AI review, Tree-sitter, RAG, LangGraph, agents, critic, Celery, Semgrep, eval, PR comments | planned |

## Prerequisites
Docker + Docker Compose (for the full stack), or Python 3.11+, Node 20+ and a local PostgreSQL 16 for development without Docker.

## Environment variables
`cp .env.example .env`. Never commit `.env`. Phase 1 only needs the database variables; GitHub, Groq/Ollama and Redis
variables are listed for later phases.

## Run with Docker
```bash
docker compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000 (health: `/health`, docs: `/docs`)

The backend container runs `alembic upgrade head` on start. Postgres uses the `pgvector/pgvector:pg16` image so
pgvector is ready for Phase 6.

## Run without Docker
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head            # migrations
uvicorn app.main:app --reload
cd ../frontend && npm install && npm run dev
```

## Tests
Backend tests use the real PostgreSQL in `DATABASE_URL` (migrate first):
```bash
cd backend && alembic upgrade head && python -m pytest
```

## Database
Tables so far: `users`, `github_accounts`, `repositories`, `pull_requests`, `reviews`, `findings`.
`code_chunks` (pgvector) arrives with RAG in Phase 6. Create new migrations with
`alembic revision --autogenerate -m "message"`.

## Troubleshooting
- `/health` returns 503: Postgres is unreachable; check `DATABASE_URL` and that migrations ran.
- `No module named 'app'` when running alembic: run it from `backend/`.
- Port 5432 already in use: stop the local Postgres or change the published port in `docker-compose.yml`.
