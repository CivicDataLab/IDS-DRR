# IDS-DRR — Intelligent Data Solution for Disaster Risk Reduction

[![Documentation Status](https://readthedocs.org/projects/ids-drr/badge/?version=latest)](https://ids-drr.readthedocs.io/en/latest/?badge=latest)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)

**IDS-DRR** is an open-source platform that helps state-level and district-level Disaster Management Authorities make timely, data-driven decisions. It joins up government spending data with complex datasets spanning flood hazard, exposure, and vulnerability — enabling decision-makers to identify where the most urgent interventions are needed and what investments have already been made.

The platform was initiall built for Assam, India, as a 4-year pilot and has since been designed to be replicable for other flood-prone geographies.

> 🌐 **Live platform:** [drr.open-contracting.in](https://drr.open-contracting.in/en/analytics?indicator=risk-score&time-period=2023_08&boundary=district)
> 📖 **Full documentation:** [ids-drr.readthedocs.io](https://ids-drr.readthedocs.io/en/latest/)

---

## Why This Exists

Floods are the most frequent natural disaster globally. In the last decade, 87% of disaster-related deaths in India were caused by floods. Yet disaster risk reduction decisions are often fragmented — information is siloed across agencies, in different systems and formats, making it hard to act quickly or equitably.

IDS-DRR breaks down those silos by bringing together:

- Satellite and environmental data
- Social, economic, and demographic indicators
- Infrastructure and loss & damage records
- Government procurement and spending data

The result is an interactive map and reporting tool that gives decision-makers a clear, evidence-based picture of flood risk — down to the revenue-circle level.

---

## Repository Structure

This is the **root repository** for the IDS-DRR platform. It uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to compose the full system and a `docker-compose.yml` to run everything locally.

```
IDS-DRR/
├── platform/
│   ├── frontend/          # Next.js web application (submodule)
│   └── data-management/   # Django REST API + PostGIS (submodule)
├── docs/                  # Sphinx documentation source
├── user_docs/             # End-user documentation
├── docker-compose.yml     # Full local development stack
└── .readthedocs.yaml      # ReadTheDocs build config
```

### Related Repositories

| Component | Repository | Description |
|---|---|---|
| **Frontend** | [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend) | Next.js web app with interactive maps, filters, and reports |
| **Data Management API** | [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management) | Django REST API for analytics, risk scores, and indicators |
| **Data Pipeline** | [IDS-DRR-Pipeline](https://github.com/CivicDataLab/IDS-DRR-Pipeline) | ETL pipelines for data ingestion and processing |
| **Risk Models (Adaptable for different geographes)** | [IDS-DRR-Risk-Score Model](https://github.com/CivicDataLab/risk-score-model-generic) | Statistical models for flood risk scoring (TOPSIS, DEA) |
| **DataSpace Backend** | [DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) | Optional: dataset catalog, search, and publishing |
| **QA Automation** | [IDS-DRR-QA-Automation](https://github.com/CivicDataLab/IDS-DRR-QA-Automation) | Optional: Automated testing and quality assurance |

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git (with submodule support)

### 1. Clone with submodules

```bash
git clone --recurse-submodules https://github.com/CivicDataLab/IDS-DRR.git
cd IDS-DRR
```

If you already cloned without `--recurse-submodules`, run:

```bash
git submodule update --init --recursive
```

### 2. Configure

```bash
cp platform/data-management/report_config.local.json platform/data-management/report_config.json
```

No `.env` files are needed — all services have sensible development defaults.

### 3. Start the stack

```bash
docker compose up -d --build
```

This brings up four services: **PostGIS** (port 54321), **Redis** (port 6380), the **Django backend** (port 8000), and the **Next.js frontend** (port 3000).

### 4. Initialize the database

```bash
docker exec context_layer_Backend python manage.py makemigrations
docker exec context_layer_Backend python manage.py migrate
docker exec context_layer_Backend python manage.py import_data
```

### 5. Open the app

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |

### Optional: DataSpace Backend

The DataSpace backend enables the dataset catalog, search, and publishing features. See the [DataSpaceBackend repository](https://github.com/CivicDataLab/DataSpaceBackend) for setup, then create `platform/frontend/.env.local`:

```env
BACKEND_URL="http://localhost:8001"
NEXT_PUBLIC_BACKEND_URL="http://localhost:8001"
```

---

## System Architecture

The platform follows an eight-stage data pipeline from raw data sources to a published, interactive front-end:

```
Identify → Collect → Process → Model → Analyze → Front-End → Publish → List
```

1. **Identify** — Determine required data, sources, and variables
2. **Collect** — Gather raw data via APIs, QGIS, or scraping
3. **Process** — Clean, transform, and standardize data into a PostGIS database
4. **Model** — Run flood risk scoring 
5. **Analyze** — Expose results through REST APIs
6. **Front-End** — Interactive maps and tailored reports for decision-makers
7. **Publish** — Historical and real-time data publishing via DataSpace
8. **List** — A searchable frontend catalog for published datasets

**Tech stack at a glance:**

| Layer | Technologies |
|---|---|
| Data pipeline & orchestration | RabbitMQ, Prefect |
| Data processing | Python, QGIS |
| Statistical modeling | TOPSIS, Gurobi (DEA) |
| Data sources | Google Earth Engine, government APIs and portals |
| Backend API | Django, PostGIS, Redis |
| Frontend | Next.js |
| Infrastructure | Docker, Docker Compose |

For a deeper dive, see the [Architecture Overview](https://ids-drr.readthedocs.io/en/latest/architecture/overview.html) in the docs.

---

## Data Model

The risk scoring framework is built around four pillars:

- **Hazard** — Flood extent, frequency, and intensity from satellite and hydrological sources
- **Exposure** — Population, assets, and infrastructure in flood-prone areas
- **Vulnerability** — Socioeconomic indicators that determine a community's susceptibility to harm
- **Coping Capacity / Government Response** — Public investment, procurement, and response history

These inputs feed a composite **Flood Risk Score** that can be viewed at district and revenue-circle granularity.

See the [Data Model documentation](https://ids-drr.readthedocs.io/en/latest/datasources/data-model.html) for full methodology, SDG relevance, limitations, and DPG compliance notes.

---

## Contributing

We welcome contributions — whether fixing a bug, improving documentation, or extending the data model to a new state.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes and open a pull request

Please check the [open issues](https://github.com/CivicDataLab/IDS-DRR/issues) for current priorities, and read the [full documentation](https://ids-drr.readthedocs.io/en/latest/) before diving in.

---

## Partners

This 4-year project is led by **[CivicDataLab](https://civicdatalab.in/)** and **[Open Contracting Partnership](https://www.open-contracting.org/)**, focused on improving disaster risk reduction processes in India. Datasets and risk score methodology was developed in collaboration with the **Assam State Disaster Management Authority** and the **Himachal Pradesh State Disaster Management Authority**. It is supported by **Patrick J. McGovern Foundation** and **The Rockefeller Foundation**.

---

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).