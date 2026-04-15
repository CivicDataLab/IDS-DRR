# Platform Technical Documentation

This section provides technical documentation for the IDS-DRR platform components.

## Platform Components

| Component | Repository | Description |
|-----------|------------|-------------|
| **Frontend** | [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend) | User-facing web application with interactive maps and dashboards |
| **Data Management** | [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management) | Backend APIs for analytics and risk data |
| **DataSpace Backend** | [DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) | Backend APIs for datasets, search, and publishing (optional) |
| **QA Automation** | [IDS-DRR-QA-Automation](https://github.com/CivicDataLab/IDS-DRR-QA-Automation) | Automated testing and quality assurance |
| **Data Pipeline** | [IDS-DRR-Pipeline](https://github.com/CivicDataLab/IDS-DRR-Pipeline) | ETL pipelines for data ingestion and processing |
| **Risk Models (Assam)** | [IDS-DRR-Assam-Risk-Model](https://github.com/CivicDataLab/IDS-DRR-Assam-Risk-Model) | Statistical models for flood risk scoring |

## Quick Start

The root `docker-compose.yml` orchestrates the core platform via git submodules for the Frontend and Data Management, plus PostGIS and Redis.

```bash
git clone --recurse-submodules https://github.com/CivicDataLab/IDS-DRR.git
cd IDS-DRR

cp platform/data-management/report_config.local.json platform/data-management/report_config.json

docker compose up -d --build

docker exec context_layer_Backend python manage.py makemigrations
docker exec context_layer_Backend python manage.py migrate
docker exec context_layer_Backend python manage.py import_data
```

The frontend will be available at **http://localhost:3000** and the backend API at **http://localhost:8000**. No `.env` files are needed; all services have sensible defaults.

## DataSpace Backend (optional)

The core platform provides analytics maps, risk scores, indicators, and reports. The [DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) is a separate service that enables the datasets catalog, search, and publishing features in the Frontend.

See the [DataSpaceBackend repository](https://github.com/CivicDataLab/DataSpaceBackend) for setup instructions. Once running, create `platform/frontend/.env.local` to connect it, for example:

```env
BACKEND_URL="http://localhost:8001"
NEXT_PUBLIC_BACKEND_URL="http://localhost:8001"
```

## Component Documentation

- [Frontend](frontend.md)
- [Data Management API](data-management.md)
- [QA & Testing](qa-automation.md)
