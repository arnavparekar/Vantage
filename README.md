<div align="center">
  <h1>Vantage</h1>
  <p><strong>Intelligent CI/CD Analytics & Webhook Processing for GitHub Actions</strong></p>
  
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
</div>

<br />

## What is Vantage?
Vantage is a full-stack analytics platform that provides actionable insights into your GitHub Actions pipelines. It ingests real-time webhook payloads from GitHub, processes workflow run data, and visualizes CI/CD performance—helping teams identify flaky tests, optimize build durations, and track deployment success rates.

## Features
- **Real-Time Webhook Ingestion**: Securely receives and validates `workflow_run` events directly from GitHub.
- **Dynamic Analytics Dashboard**: Visualizes Mean Time To Recovery (MTTR), daily failure rates, and build duration trends.
- **Flaky Workflow Detection**: Algorithmically identifies unstable pipelines that frequently toggle between success and failure.
- **Multi-Tenant Architecture**: Add a single webhook URL to multiple repositories to monitor your entire organization from one centralized dashboard.
- **Automated Infrastructure**: Fully containerized with Docker Compose, featuring automated zero-downtime EC2 deployments via GitHub Actions.

## Tech Stack
- **Backend**: Python, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, Vite, Tailwind CSS, Recharts
- **Infrastructure**: Docker, Nginx, Prometheus, Grafana, AWS EC2
- **CI/CD**: GitHub Actions

## Architecture
1. **GitHub** sends a cryptographic webhook payload upon any Action completion.
2. **FastAPI (Backend)** validates the HMAC signature, parses the payload, and upserts the data into **PostgreSQL**.
3. **React (Frontend)** fetches aggregated metrics via the REST API to render beautiful, responsive charts.
4. **Prometheus & Grafana** run in the background to monitor API health, request latency, and HTTP error rates.

---

## Quick Start (Local Development)

### 1. Run the Full Stack with Docker
Spin up the Database, Backend, Frontend, and Observability stack in a single command:
```bash
docker compose up -d --build
```
- **Dashboard**: `http://localhost`
- **API Docs**: `http://localhost:8000/docs`
- **Grafana**: `http://localhost:3001` (User/Pass: `admin`)

### 2. Connect Your GitHub Repository
1. Navigate to your GitHub Repository -> **Settings** -> **Webhooks** -> **Add Webhook**.
2. **Payload URL**: `http://<YOUR_IP_OR_DOMAIN>/webhook/github` (Use *Ngrok* if running locally).
3. **Content type**: `application/json`.
4. Select **Let me select individual events** and check **Workflow runs**.
5. Save and re-run an old workflow to see data instantly populate your dashboard!

---
*Built with passion to bring clarity to CI/CD pipelines.*
