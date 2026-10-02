# EDXSO Influencer Outreach AI (InfluenceFlow AI)
## Phase 8: Deployment, Local Setup & Operations Guide

---

### 1. Prerequisites
- **Node.js**: `v20.x` or `v22.x`
- **npm**: `v10.x` or higher
- **Python**: `3.11` to `3.13`
- **Docker & Docker Compose** (optional for containerized deployment)

---

### 2. Local Development Setup (Bare Metal)

#### Step 1: Clone & Configure Environment
```bash
git clone <repository_url>
cd EDXSO
cp .env.example .env
```

#### Step 2: Install Python AI Service Dependencies
```bash
cd apps/ai-service
pip install -r requirements.txt
cd ../..
```

#### Step 3: Install Node.js API Gateway Dependencies
```bash
cd apps/api
npm install
cd ../..
```

#### Step 4: Install Next.js Frontend Dependencies
```bash
cd apps/web
npm install
cd ../..
```

#### Step 5: Start All Microservices Concurrently
In three separate terminal windows (or using your process manager):

```bash
# Terminal 1: Python AI Service (Port 8000)
cd apps/ai-service
python main.py

# Terminal 2: Node.js Express Gateway (Port 5000)
cd apps/api
npm run dev

# Terminal 3: Next.js Frontend UI (Port 3000)
cd apps/web
npm run dev
```

The system will be accessible at:
- **Dashboard UI**: `http://localhost:3000`
- **API Gateway**: `http://localhost:5000/health`
- **AI Microservice**: `http://localhost:8000/docs` (Interactive Swagger UI)

---

### 3. Docker Compose Deployment (Single Command)

```bash
# Build and run all microservices in isolated containers
docker-compose up --build -d

# View real-time aggregated logs
docker-compose logs -f
```

---

### 4. Operational Runbook & Dry-Run Mode

> [!NOTE]
> By default, `DRY_RUN=true` is enabled in `.env`. In this mode, no real emails are dispatched via SMTP; instead, all outreach is safely simulated and logged as `SIMULATED` in the outreach audit trail.

To enable live email dispatch:
1. In `.env`, set:
   ```env
   DRY_RUN=false
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_google_app_password
   ```
2. Restart the Node.js API Gateway service.
