# Data Management API

The Data Management component provides the backend APIs and data management layer for the IDS-DRR platform.

**Repository**: [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management)

## Features

- **Data Storage**: PostGIS-enabled PostgreSQL database for storing processed data, risk scores, and geographical boundaries
- **Caching**: Redis for caching query results (maps, tables, time trends, indicators)
- **API Endpoints**: GraphQL APIs (via Strawberry) for frontend data access
- **Data Ingestion**: Django management commands for importing geographical and indicator data
- **Geographical Data**: Support for states, districts, revenue circles, sub-districts, blocks, and tehsils

## Tech stack

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

## Local development

### Option 1: Using Docker (recommended)

The `docker-compose.yml` file provides three services:

| Service | Container | Host port | Description |
|---|---|---|---|
| `db` | `context_layer_PG` | `54321` | PostGIS database |
| `redis` | `context_layer_Redis` | `6380` | Redis cache |
| `web` | `context_layer_Backend` | `8000` | Django application |

1. Clone the repository:

   ```bash
   git clone https://github.com/CivicDataLab/IDS-DRR-Data-Management.git
   cd IDS-DRR-Data-Management
   ```

2. Start services:

   ```bash
   docker compose up -d --build
   ```

3. Run migrations:

   ```bash
   docker exec context_layer_Backend python manage.py makemigrations
   docker exec context_layer_Backend python manage.py migrate
   ```

4. Import data (see [Data import](#data-import) below):

   ```bash
   docker exec context_layer_Backend python manage.py import_geojson
   docker exec context_layer_Backend python manage.py import_indicators
   docker exec context_layer_Backend python manage.py import_data
   ```

The API will be available at <http://localhost:8000>.

To override the default settings (e.g. credentials), create a `.env` file in the project root; Docker Compose picks it up automatically. See [Environment Variables](#environment-variables) below.

### Option 2: Manual setup

1. Clone the repository:

   ```bash
   git clone https://github.com/CivicDataLab/IDS-DRR-Data-Management.git
   cd IDS-DRR-Data-Management
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file (see [Environment variables](#environment-variables) below). For a manual setup where Postgres and Redis run on the host, set `POSTGRES_HOST=localhost` and `REDIS_URL=redis://127.0.0.1:6379/1`.

5. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Import data (see [Data import](#data-import) below):

   ```bash
   python manage.py import_geojson
   python manage.py import_indicators
   python manage.py import_data
   ```

7. Start the development server:

   ```bash
   python manage.py runserver
   ```

The API will be available at <http://localhost:8000>.

## Configuration

The Data Management component reads deployment-specific data from a TOML file at startup. The default path is `config.toml` next to `manage.py` (override with the `CONFIG_PATH` environment variable).

### Prepare your config

1. Copy [config.toml.example](https://github.com/CivicDataLab/IDS-DRR-Data-Management/blob/dev/config.toml.example) to `config.toml` next to `manage.py`. It's annotated inline; lean on the comments as you fill out the sections below.
2. Add a `[[geojson]]` entry for each geography level you want to import (state, district, sub-district, etc.). Each entry points at a GeoJSON file, declares the geography type, and describes how to derive each feature's code from its properties.
3. Add a `[[states]]` entry for each region you're shipping. Each entry points at that region's indicator-definition and indicator-value CSVs, plus any optional metadata.
4. Adjust top-level options (`whitelist_indicators`, `default_time_period`, `simplify_tolerance`, `[[chart_types]]` for [DataSpace map charts](dataspace.md#adding-a-new-map-chart), etc.) as needed for your deployment.

### Directory layout

Lay out your deployment directory so `config.toml` sits at the root and references its siblings:

```
<your-deployment>/
  config.toml
  geography/
    <your>.geojson
  indicators/
    <state>_indicators.csv
  data/
    <state>_data.csv
```

Paths in `config.toml` are written relative to it, e.g. `path = "geography/foo.geojson"`.

Deployments that ship a [plugin](#pdf-report-opt-in) can keep its code alongside the config + data so everything is versioned together. The IDS-DRR India deployment, for example, does this in [ids-drr-india-plugin](https://github.com/CivicDataLab/ids-drr-india-plugin). Deployments without a plugin can keep config + data in a standalone directory.

### Check your config

The TOML file's schema is enforced at startup: errors like unknown keys or malformed `[[geojson]]` parent specs raise `ImproperlyConfigured`. A `layer.W001` system check warns when no configuration is loaded, and `layer.W002.<section>` warns when the `[[geojson]]` or `[[states]]` sections are missing. Run `python manage.py check` to check for any warnings.

### Load your config in Docker Compose

Add your deployment directory as a new bind-mount on the `web` service, alongside the existing source-code mount:

```{code-block} yaml
:emphasize-lines: 5

services:
  web:
    volumes:
      - ./platform/data-management:/code
      - ./<your-deployment>:/config:ro
```

Then set `CONFIG_PATH=/config/config.toml` in the `web` service's environment: either in the compose `environment:` block, or in a `.env` file picked up via `env_file:`.

Inside the container, the TOML lives at `/config/config.toml`, so its relative paths resolve to `/config/geography/…`, `/config/data/…`, etc.

### Load your config without Docker

Set `CONFIG_PATH` in your `.env` (or the process' environment) to either a relative or absolute path:

```
CONFIG_PATH=path/to/deployment/config.toml
```

### PDF report (opt-in)

The frontend can render a "Download Report" button on the analytics page that fetches a PDF from this backend's `/report` endpoint; see [Frontend → PDF Report (opt-in)](frontend.md#pdf-report-opt-in) for the user-facing behaviour and the API contract the frontend expects.

The Data Management component does **not** ship a `/report` implementation; deployments that want one provide it as a Django app (a "plugin"). The Data Management component always loads this Django app at the module name `plugin`.

The Data Management component provides a default plugin, `plugin-stub`, which ships no routes, so the platform exposes no PDF endpoint. To expose one, install a deployment-specific plugin in place of the stub. See [ids-drr-india-plugin](https://github.com/CivicDataLab/ids-drr-india-plugin) for a worked example.

To enable a plugin:

1. Install it into the data-management environment in place of `plugin-stub`. For example:

   ```bash
   uv pip install --force-reinstall --no-deps <path-to-plugin>
   ```

2. Set `features.reports = true` in the frontend branding package's `src/config.ts` so the "Download Report" button is shown. For more, see [Frontend → PDF Report (opt-in)](frontend.md#pdf-report-opt-in).

If the frontend button is enabled but no real plugin is installed (or the stub is still in place), "Download Report" clicks return 404.

## Environment variables

When using Docker, all variables have sensible defaults; no `.env` file is needed. To override any value, create a `.env` file in the project root; Docker Compose picks it up automatically.

For manual (non-Docker) setup, a `.env` file is required since there are no defaults for database connection details.

| Variable | Description | Docker Compose default | Manual setup value |
|----------|-------------|---------|-------------------|
| `POSTGRES_NAME` | Database name | `postgres` | your database name |
| `POSTGRES_USER` | Database user | `postgres` | your database user |
| `POSTGRES_PASSWORD` | Database password | `postgres` | your database password |
| `POSTGRES_HOST` | Database host | `db` | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` | `5432` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/1` | `redis://127.0.0.1:6379/1` |

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

## Data import

The Data Management component uses three management commands that must be run in order. Each stage assumes the previous one has populated its prerequisite rows:

```bash
python manage.py import_geojson      # geographies
python manage.py import_indicators   # indicator definitions
python manage.py import_data         # indicator values
```

`import_indicators` and `import_data` accept `--state "<name>"` to restrict the run to one state (must match a `[[states]]` entry exactly; run `--help` to see the list). `import_data` also accepts `--district <code>` to restrict the run to one district:

```bash
python manage.py import_indicators --state Assam
python manage.py import_data --state Assam --district 201
```

Running `import_data` for a state that has no indicators yet (or whose indicator slugs don't overlap with any columns in the data CSV) raises a `CommandError` rather than silently importing nothing.

### What the import commands do

1. **`import_geojson`** reads `[[geojson]]` from `config.toml` and inserts `Geography` rows (state, district, sub-district) with their MultiPolygon geometries. Per-file code extraction and parent lookup are driven by the TOML; see the comments in `config.toml.example`.
2. **`import_indicators`** reads each `[[states]]` entry's [indicators CSV](#indicator-csv-schema) and upserts `Indicators` rows for that state (name, description, category, unit, data source, parent, visibility).
3. **`import_data`** reads each `[[states]]` entry's [data CSV](#data-csv-schema) and inserts `Data` rows, one per (indicator, geography, time period). Existing rows for the affected geographies and time periods are deleted first.

### Resetting before a new config

To load a different `config.toml` from scratch, wipe the imported rows first:

```bash
python manage.py delete_imports
```

This deletes every `Data`, `Indicators`, `Unit`, and `Geography` row in a foreign-key-safe order and invalidates the data cache. It prompts for confirmation; pass `--noinput` to skip the prompt.

### Indicator CSV schema

The indicator CSV is the platform's public API for loading indicators; column names are fixed. Pre-process your source data to match before pointing `config.toml` at it.

| Column | Description |
|--------|-------------|
| `indicatorSlug` | Unique identifier for the indicator (lower-cased on import). |
| `indicatorTitle` | Display name of the indicator. |
| `indicatorDescription` | Detailed description. |
| `indicatorCategory` | Category grouping. |
| `unit` | Unit of measurement. Matched against `Unit.name`, case-insensitive; created on first use. |
| `datasource` | Data source reference (free text). |
| `parent` | Display name of the parent indicator within the same state, if any. |
| `visible_on_platform` | `y` to expose the indicator on the platform, otherwise hidden. |

### Data CSV schema

Likewise, the data CSV schema is fixed:

| Column | Description |
|--------|-------------|
| `object-id` | Geography code — used as the CSV index; must match a `Geography.code` imported from GeoJSON. |
| `timeperiod` | Time period for the row (e.g. `2024_08`). |
| *`<indicatorSlug>`* | One column per indicator slug, holding that row's value. Extra columns are ignored. |

## Troubleshooting

### Common issues

1. **PostGIS Extension Missing**: Ensure PostgreSQL has the PostGIS extension installed.

   ```sql
   CREATE EXTENSION postgis;
   ```

2. **GDAL/GEOS Not Found**: Install geospatial libraries.

   ```bash
   # Ubuntu/Debian
   apt-get install gdal-bin python3-gdal libgeos-dev libproj-dev
   
   # macOS
   brew install gdal geos proj
   ```

3. **State data file missing**: Each `[[states]]` entry's `data` path in `config.toml` must resolve to an existing CSV. Paths are relative to the TOML file.
