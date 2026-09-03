# Convenience targets. You can also run the raw commands in the README.

backend-setup:
	cd backend && python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

backend:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000

frontend-setup:
	cd frontend && npm install

frontend:
	cd frontend && npm run dev

.PHONY: backend-setup backend frontend-setup frontend
