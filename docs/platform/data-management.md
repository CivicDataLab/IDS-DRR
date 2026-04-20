# Data Management API

The Data Management component provides the backend APIs and data management layer for the IDS-DRR platform.

**Repository**: [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management)

## Overview

The Data Management layer handles:

- **Data Storage**: PostGIS-enabled PostgreSQL database for storing processed data, risk scores, and geographical boundaries
- **Caching**: Redis for caching query results (maps, tables, time trends, indicators)
- **API Endpoints**: GraphQL APIs (via Strawberry) for frontend data access
- **Data Ingestion**: Django management commands for importing geographical and indicator data
- **Geographical Data**: Support for states, districts, revenue circles, sub-districts, blocks, and tehsils

## Tech Stack

- **Framework**: Django 4.2
- **Database**: PostgreSQL with PostGIS extension
- **Cache**: Redis
- **API**: Strawberry GraphQL
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.12+
- PostgreSQL with PostGIS extension
- Redis
- GDAL, GEOS, and PROJ libraries (for geospatial operations)
- Docker & Docker Compose (recommended)

## Local Development

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/CivicDataLab/IDS-DRR-Data-Management.git
cd IDS-DRR-Data-Management

# Create report configuration (required for state listing and PDF reports)
cp report_config.local.json report_config.json

# Start services
docker compose up -d --build

# Run migrations
docker exec context_layer_Backend python manage.py makemigrations
docker exec context_layer_Backend python manage.py migrate

# Import data (see Data Import section below)
docker exec context_layer_Backend python manage.py import_data

# The API will be available at http://localhost:8000
```

To override the defaults (e.g. credentials), create a `.env` file in the project root; Docker Compose picks it up automatically. See [Environment Variables](#environment-variables) below.

See `report_config.example.json` for the full configuration format, including report sections and chart definitions.

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/CivicDataLab/IDS-DRR-Data-Management.git
cd IDS-DRR-Data-Management

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file and configure (see Environment Variables below)
# Set POSTGRES_HOST=localhost and REDIS_URL=redis://127.0.0.1:6379/1
# for a manual setup where Postgres and Redis run on the host

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Import data (see Data Import section below)
python manage.py import_data

# Start development server
python manage.py runserver
```

## Environment Variables

When using Docker, all variables have sensible defaults; no `.env` file is needed. To override any value, create a `.env` file in the project root; Docker Compose picks it up automatically for variable substitution.

For manual (non-Docker) setup, a `.env` file is required since there are no defaults for database connection details.

| Variable | Description | Docker Compose default | Manual setup value |
|----------|-------------|---------|-------------------|
| `POSTGRES_NAME` | Database name | `postgres` | your database name |
| `POSTGRES_USER` | Database user | `postgres` | your database user |
| `POSTGRES_PASSWORD` | Database password | `postgres` | your database password |
| `POSTGRES_HOST` | Database host | `db` | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/1` | `redis://127.0.0.1:6379/1` |
| `CHART_API_BASE_URL` | DataSpace chart generation endpoint, used to render charts as images in PDF reports (e.g. `http://localhost:8001/api/generate-dynamic-chart/`) | | |
| `WHITELIST_INDICATORS` | Comma-separated indicator slugs to import in addition to visible indicators | `topsis-score` | `topsis-score` |

### Production

| Variable | Description |
|----------|-------------|
| `DJANGO_ENV` | Set to `production` to disable debug mode by default. |
| `SECRET_KEY` | Django secret key, used for cryptographic signing. Must be set to a unique, unpredictable value in production. The default (`!!!SECRET_KEY!!!`) is not safe for production. |
| `ALLOWED_HOSTS` | Comma-separated list of hostnames the server will accept requests for, appended to the built-in defaults (`localhost`, `127.0.0.1`, `0.0.0.0`). Must include the domain(s) serving the API. |
| `DEBUG` | Enable Django debug mode. Defaults to `True` unless `DJANGO_ENV=production`. Set to `True` or `False` explicitly to override. |

Generate a secret key with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Data Import

The data management layer uses the `import_data` management command for importing and updating data.

Import all data (geojson, indicators, and data for all states):

```bash
python manage.py import_data
```

Or, import data for a specific state:

```bash
python manage.py import_data --state assam
python manage.py import_data --state himachal_pradesh
python manage.py import_data --state odisha
```

Or, import data for a specific district within a state:

```bash
python manage.py import_data --state assam --district 201
```

### What the Import Command Does

1. **Migrates GeoJSON Data**: Imports geographical boundaries from `layer/assets/geojson/` directory
   - Creates state, district, revenue circle, sub-district, block, and tehsil records
   - Stores MultiPolygon geometries for each geographical unit

2. **Updates Indicators**: Imports indicator definitions from `layer/assets/indicators/*_indicators.csv`
   - Creates/updates indicator metadata (name, description, category, unit, data source)
   - Links indicators to their parent indicators and geographical units

3. **Imports State Data**: Imports actual data values from `layer/assets/data/*_data.csv`
   - Associates data values with indicators and geographical units
   - Supports time-period based data

### Indicator CSV Format

The indicator CSV files should have the following columns:

| Column | Description |
|--------|-------------|
| `indicatorSlug` | Unique identifier for the indicator |
| `indicatorTitle` | Display name of the indicator |
| `indicatorDescription` | Detailed description |
| `indicatorCategory` | Category grouping |
| `unit` | Unit of measurement |
| `datasource` | Data source reference |
| `parent` | Parent indicator name (for hierarchical indicators) |
| `visible_on_platform` | `y` or `n` to control visibility |

### Data CSV Format

The data CSV files should have:

- `object-id`: Geography code (used as index)
- `timeperiod`: Time period for the data (e.g., `2024_08`)
- Columns for each indicator slug with their values

## Database Schema

### Core Models

- **Geography**: Stores geographical boundaries (states, districts, etc.) with PostGIS geometry
- **Indicators**: Stores indicator metadata and hierarchical relationships
- **Data**: Stores actual data values linked to indicators and geographies
- **Unit**: Stores units of measurement

## Docker Services

The `docker-compose.yml` provides three services:

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| `db` | `context_layer_PG` | `54321:5432` | PostGIS database |
| `redis` | `context_layer_Redis` | `6380:6379` | Redis cache |
| `web` | `context_layer_Backend` | `8000:8000` | Django application |

## Troubleshooting

### Common Issues

1. **PostGIS Extension Missing**: Ensure PostgreSQL has PostGIS extension installed

   ```sql
   CREATE EXTENSION postgis;
   ```

2. **GDAL/GEOS Not Found**: Install geospatial libraries

   ```bash
   # Ubuntu/Debian
   apt-get install gdal-bin python3-gdal libgeos-dev libproj-dev
   
   # macOS
   brew install gdal geos proj
   ```

3. **State Data File Missing**: Ensure data files exist in `layer/assets/data/` with correct naming convention (`{state}_data.csv`)
