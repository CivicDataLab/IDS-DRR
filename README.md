# IDS-DRR — Intelligent Data Solution for Disaster Risk Reduction

[![Documentation Status](https://readthedocs.org/projects/ids-drr/badge/?version=latest)](https://ids-drr.readthedocs.io/en/latest/?badge=latest)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](LICENSE)

**IDS-DRR** is an open-source platform that helps state-level and district-level Disaster Management Authorities make timely, data-driven decisions. It joins up government spending data with complex datasets spanning hazard, exposure, vulnerability, and coping capacity — enabling decision-makers to identify where the most urgent interventions are needed and what investments have already been made.

The platform was initially built for Assam, India, as a 4-year pilot and has since been designed to be replicable for other regions.

> 🌐 **Live platform:** [drr.open-contracting.in](https://drr.open-contracting.in/en/analytics?indicator=risk-score&time-period=2023_08&boundary=district)
> 📖 **Full documentation:** [ids-drr.readthedocs.io](https://ids-drr.readthedocs.io/en/latest/)

---

## Why this exists

Disaster risk reduction decisions are often fragmented — information is siloed across agencies, in different systems and formats, making it hard to act quickly or equitably.

IDS-DRR breaks down those silos by bringing together:

- Satellite and environmental data
- Social, economic, and demographic indicators
- Infrastructure and loss & damage records
- Government procurement and spending data

The result is an interactive map that gives decision-makers a clear, evidence-based picture of risk down to the sub-district level. The risk-scoring methodology is hazard-agnostic — the same framework supports floods, cyclones, droughts, earthquakes, and other natural hazards, with different input indicators per hazard.

### Reference deployment: Assam flood pilot

> [!NOTE]
> The first deployment was a 4-year pilot in Assam, India, focused on **floods**. Floods are the most frequent natural disaster globally — in the last decade, 87% of disaster-related deaths in India were caused by floods. The Assam pilot has since been replicated with state authorities in Odisha, Uttar Pradesh, Bihar, and Himachal Pradesh.

---

## Repository structure

This is the **root repository** for the IDS-DRR platform. It uses [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) to compose the full system and a `docker-compose.yml` to run everything locally.

```
IDS-DRR/
├── platform/
│   ├── frontend/                  # Next.js web application (submodule)
│   ├── data-management/           # Django + PostGIS (submodule)
│   └── risk-score-model-generic/  # Python risk-scoring model (submodule)
├── docs/                          # Sphinx documentation source
├── user_docs/                     # End-user documentation
├── docker-compose.yml             # Full local development stack
└── .readthedocs.yaml              # ReadTheDocs build config
```

### Related repositories

| Component | Repository | Description |
|---|---|---|
| Frontend | [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend) | Next.js web app with interactive maps, filters, and reports |
| Data Management API | [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management) | Django REST API for analytics, risk scores, and indicators |
| Risk-score model | [risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic) | Generic, methodology-driven scoring model (TOPSIS, DEA) |
| DataSpace Backend | [DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) | Optional: dataset catalog, search, and publishing |
| QA Automation | [IDS-DRR-QA-Automation](https://github.com/CivicDataLab/IDS-DRR-QA-Automation) | Optional: automated testing and quality assurance |

For each component's docs, see [Platform components](https://ids-drr.readthedocs.io/en/latest/platform/#platform-components).

---

## Quick start

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

No `.env` files are needed — all services have sensible development defaults.

### 2. Start the stack

```bash
docker compose up -d --build
```

This brings up four services: **PostGIS** (port 54321), **Redis** (port 6380), the **Django backend** (port 8000), and the **Next.js frontend** (port 3000).

### 3. Initialize the database

```bash
docker exec context_layer_Backend python manage.py makemigrations
docker exec context_layer_Backend python manage.py migrate
docker exec context_layer_Backend python manage.py import_geojson
docker exec context_layer_Backend python manage.py import_indicators
docker exec context_layer_Backend python manage.py import_data
```

### 4. Open the app

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |

### Optional: DataSpace Backend

The DataSpace backend enables the analytics page's chart view and the datasets catalog. See [DataSpace Integration](https://ids-drr.readthedocs.io/en/latest/platform/dataspace.html) for how to wire it in.

---

## Documentation

- [Risk-scoring methodology](https://ids-drr.readthedocs.io/en/latest/datasources/data-model.html): SENDAI framework, factor scoring, DEA
- [Data lifecycle](https://ids-drr.readthedocs.io/en/latest/architecture/overview.html)
- [Platform overview](https://ids-drr.readthedocs.io/en/latest/platform/): components, localization, deployment
- [Adopting the platform for a new region](https://ids-drr.readthedocs.io/en/latest/platform/#localizing-ids-drr)

---

## Contributing

We welcome contributions. See the [Contributing](https://ids-drr.readthedocs.io/en/latest/platform/contributing.html) page for issue trackers and contact info, and the [Development](https://ids-drr.readthedocs.io/en/latest/platform/development.html) page for design notes for code contributors.

---

## Partners

This 4-year project is led by **[CivicDataLab](https://civicdatalab.in/)** and **[Open Contracting Partnership](https://www.open-contracting.org/)**, focused on improving disaster risk reduction processes in India. Datasets and risk-score methodology were developed in collaboration with the **Assam State Disaster Management Authority** and the **Himachal Pradesh State Disaster Management Authority**. It is supported by **The Rockefeller Foundation** and the **Patrick J. McGovern Foundation**.

---

## License

This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
