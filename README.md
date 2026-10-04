# AI-Based Medical Image Diagnosis & Triage Support System

This system is an AI-assisted screening tool that flags high-risk cases from chest X-rays and dermatoscopic skin images, helping prioritize patients for specialist review. It is explicitly a **triage / decision-support tool**, not a diagnostic replacement.

## Project Structure

```text
PROJECT/
├── docker-compose.yml             # Orchestrates the containers
├── README.md                      # Setup & usage guide
├── ml_service/                    # Python FastAPI ML microservice
└── backend/                       # Node.js/Express coordination server
└── frontend/                      # React frontend dashboard (Vite)
```

## Running the Application

Ensure you have Docker and Docker Compose installed.

1. **Start all services**:
   ```bash
   docker-compose up --build
   ```

2. **Access the components**:
   *   **Frontend Dashboard**: `http://localhost:5173`
   *   **Express Backend Server**: `http://localhost:5000`
   *   **FastAPI ML Microservice**: `http://localhost:8000` (docs at `http://localhost:8000/docs`)

## Ethical Disclaimer
This system is a decision-support / triage tool, not a diagnostic replacement for a licensed radiologist or dermatologist. It is trained exclusively on public, de-identified research datasets (NIH ChestX-ray14, ISIC, HAM10000).
