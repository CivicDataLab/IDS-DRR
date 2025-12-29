# Data Management API

The Data Management component provides the backend APIs and data management layer for the IDS-DRR platform.

**Repository**: [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management)

## Overview

The Data Management layer handles:

- **Data Storage**: PostGIS-enabled PostgreSQL database for storing processed data, risk scores, and geographical boundaries
- **API Endpoints**: GraphQL APIs (via Strawberry) for frontend data access
- **Data Ingestion**: Django management commands for importing geographical and indicator data
- **Geographical Data**: Support for states, districts, revenue circles, sub-districts, blocks, and tehsils

## Tech Stack

- **Framework**: Django 4.2
- **Database**: PostgreSQL with PostGIS extension
- **API**: Strawberry GraphQL
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Python 3.12+
- PostgreSQL with PostGIS extension
- GDAL, GEOS, and PROJ libraries (for geospatial operations)
- Docker & Docker Compose (optional, for containerized setup)

## Local Development

### Option 1: Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/CivicDataLab/IDS-DRR-Data-Management.git
cd IDS-DRR-Data-Management

# Create environment file
cp .env.example .env
# Edit .env with your configuration

# Start services
docker-compose up -d

# The API will be available at http://localhost:8000
```

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

# Create environment file and configure
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_NAME` | Database name | `idsdrr_db` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `your_password` |
| `POSTGRES_HOST` | Database host | `localhost` or `db` (Docker) |
| `POSTGRES_PORT` | Database port | `5432` |
| `STATE_LIST` | Comma-separated list of states | `Assam,Himachal Pradesh,Odisha` |
| `CHART_API_BASE_URL` | Base URL for chart API | `http://localhost:3000` |
| `DATA_RESOURCE_MAP_18` | Data resource for Assam (code 18) | `resource_id` |
| `DATA_RESOURCE_MAP_21` | Data resource for Odisha (code 21) | `resource_id` |
| `DATA_RESOURCE_MAP_02` | Data resource for HP (code 02) | `resource_id` |

## Data Update via manage.py

The data management layer uses Django management commands for importing and updating data. The primary command is `import_data`.

### Import Data Command

```bash
# Import all data (geojson, indicators, and data for all states)
python manage.py import_data

# Import data for a specific state
python manage.py import_data --state assam
python manage.py import_data --state himachal_pradesh
python manage.py import_data --state odisha

# Import data for a specific district within a state
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

### Data File Structure

```text
layer/assets/
├── geojson/
│   ├── assam_district.geojson
│   ├── assam_revenue_circles_nov2022.geojson
│   ├── BharatMaps_HP_district.geojson
│   ├── bharatmaps_HP_subdistricts.geojson
│   ├── hp_tehsil_temp.geojson
│   ├── odisha_district.geojson
│   └── odisha_block.geojson
├── indicators/
│   ├── assam_indicators.csv
│   ├── himachal_pradesh_indicators.csv
│   └── odisha_indicators.csv
└── data/
    ├── assam_data.csv
    ├── himachal_pradesh_data.csv
    └── odisha_data.csv
```

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

The `docker-compose.yml` provides two services:

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| `db` | `context_layer_PG` | `54321:5432` | PostGIS database |
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
