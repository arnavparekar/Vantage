# Vantage

Vantage is a full-stack CI/CD Analytics and Webhook processing application designed to track, visualize, and analyze GitHub Actions workflows. 

## Tech Stack
- **Backend:** FastAPI, Python, SQLAlchemy, PostgreSQL
- **Frontend:** React, Vite, Tailwind CSS, Recharts
- **Infra:** Docker Compose, Prometheus, Grafana, Nginx
- **CI/CD:** GitHub Actions

## Local Setup

### 1. Environment Variables
Create a `.env` file in the root directory (this is automatically loaded by docker-compose) or set them in your environment:
```env
POSTGRES_DB=Vantage
POSTGRES_USER=Vantage
POSTGRES_PASSWORD=Vantage
GITHUB_WEBHOOK_SECRET=your_github_webhook_secret
GF_SECURITY_ADMIN_PASSWORD=admin
```

### 2. Running the Full Stack (Docker)
To spin up the entire system (Database, Backend, Frontend, Prometheus, Grafana, Nginx):
```bash
docker compose up -d --build
```
- **Frontend:** http://localhost:80 (via Nginx)
- **Backend API Docs:** http://localhost:8000/docs
- **Prometheus:** http://localhost:9090
- **Grafana:** http://localhost:3001 (User: `admin` / Password: `admin`)

### 3. Running for Local Development (Without Docker)
**Backend:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="sqlite:///./test.db"
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## GitHub Webhooks Integration
Go to your GitHub repository -> Settings -> Webhooks -> Add Webhook.
- **Payload URL:** `https://your-domain.com/webhook/github` (or use ngrok locally: `ngrok http 8000`)
- **Content type:** `application/json`
- **Secret:** Match the `GITHUB_WEBHOOK_SECRET` in your `.env`
- **Events:** Select "Workflow runs"

## Deployment to EC2
The CI/CD pipeline (`.github/workflows/ci-cd.yml`) handles deployment automatically when pushing to the `main` branch.
Ensure you have set the following secrets in your GitHub repository:
- `EC2_HOST`
- `EC2_USER`
- `EC2_SSH_KEY`
