# Platform Technical Documentation

This section provides technical documentation for the IDS-DRR platform components, geared at teams looking to either contribute to the codebase or adopt the platform for their own region.

## Is this for me?

IDS-DRR adapts to your region's data, language, and branding.

The platform is designed for teams that:

- Operate (or partner with) a sub-national disaster management authority or equivalent body.
- Want to publish a public-facing risk-analytics website backed by their own data.
- Have or can acquire **administrative boundary geometries** (GeoJSON) and **periodic indicator data** (monthly is typical) for hazard, exposure, vulnerability, and coping-capacity factors.
- Have a developer (or contractor) comfortable with Docker, Django, Node.js, and basic geospatial tooling.

Two reference deployments demonstrate this:

- **India**: The original deployment, covering Assam, Bihar, Himachal Pradesh, Odisha, and Uttar Pradesh. Lives in [ids-drr-india-plugin](https://github.com/CivicDataLab/ids-drr-india-plugin) (backend config and Django plugin) and [ids-drr-india-branding](https://github.com/CivicDataLab/ids-drr-india-branding) (frontend branding package).
- **Paraguay**: A multilingual (Spanish and Guaraní) deployment showing portability to other countries and languages. The `ids-drr-paraguay-data` (backend) and `ids-drr-paraguay-branding` (frontend) directories live within [open-contracting/data-support](https://github.com/open-contracting/data-support).

## Risk model

IDS-DRR is built around the UN [SENDAI framework](https://www.undrr.org/implementing-sendai-framework/what-sendai-framework) for Disaster Risk Reduction, which defines risk as a function of four factors:

```text
Risk ∝ Exposure × Hazard × Vulnerability × (lack of Coping Capacity)
```

Each factor scores 1–5; the overall risk score is computed monthly per administrative unit. The methodology is **not** flood-specific; adopters scoring other hazards (cyclone, drought, earthquake) reuse the same framework with different input indicators.

- [Data Model](../datasources/data-model.md) — full methodology: factor definitions, normalization, z-score binning, and Data Envelopment Analysis for vulnerability.
- [Data Sources](../datasources/data-ingestion.md) — the data sources used by the IDS-DRR India deployment, as a reference for the kinds of inputs each factor expects.
- [risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic) — the implementation. Produces the indicator-values CSV that `manage.py import_data` consumes.

## Platform components

| Component | Repository | Docs | Description |
|-----------|------------|------|-------------|
| **Frontend** | [IDS-DRR-Frontend](https://github.com/CivicDataLab/IDS-DRR-Frontend) | [Frontend](frontend.md) | User-facing web application with interactive maps and dashboards |
| **Data Management** | [IDS-DRR-Data-Management](https://github.com/CivicDataLab/IDS-DRR-Data-Management) | [Data Management API](data-management.md) | Backend APIs for analytics and risk data |
| **Risk-score model** | [risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic) | [Risk model](#risk-model) | Generic, methodology-driven scoring model used to produce indicator values |
| **DataSpace Backend** | [DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) | [DataSpace Integration](dataspace.md) | Datasets catalog, search, and chart visualisations (optional) |
| **QA Automation** | [IDS-DRR-QA-Automation](https://github.com/CivicDataLab/IDS-DRR-QA-Automation) | [QA & Automation](qa-automation.md) | Automated testing and quality assurance |

## Quick-start

The [IDS-DRR repository](https://github.com/CivicDataLab/IDS-DRR) ties the core platform together via its [docker-compose.yml](https://github.com/CivicDataLab/IDS-DRR/blob/main/docker-compose.yml). **Frontend** and **Data Management** are git submodules of that repository; the **risk-score model** and per-deployment branding/data packages are separate repositories to clone alongside as needed.

```bash
git clone --recurse-submodules https://github.com/CivicDataLab/IDS-DRR.git
cd IDS-DRR

docker compose up -d --build

docker exec context_layer_Backend python manage.py makemigrations
docker exec context_layer_Backend python manage.py migrate
docker exec context_layer_Backend python manage.py import_geojson
docker exec context_layer_Backend python manage.py import_indicators
docker exec context_layer_Backend python manage.py import_data
```

The frontend will be available at **http://localhost:3000** and the backend API at **http://localhost:8000**. No `.env` files are needed; all services have sensible defaults.

## Localizing IDS-DRR

Adapting IDS-DRR to your region involves four pieces of work. The platform handles the application code, schema enforcement, query caching, and rendering; adoption is about producing the right inputs and branding.

1. **Assemble administrative boundaries.** Collect GeoJSON for each geography level you want to show (state/province, district, sub-district). These are imported by `manage.py import_geojson` and stored as PostGIS MultiPolygons.

2. **Prepare indicator data.** For each region, produce two CSVs: indicator definitions in the fixed [8-column schema](data-management.md#indicator-csv-schema), and indicator values indexed by `object-id` × `timeperiod` in the [data CSV format](data-management.md#data-csv-schema). The values come from the [risk-score model](#risk-model), run by you or supplied by whoever owns the methodology for your region.

3. **Write the backend configuration.** A `config.toml` ties together the GeoJSON, the per-region CSVs, the indicator whitelist, and any feature flags. See [Data Management → Configuration](data-management.md#configuration).

4. **Build a frontend branding package.** A small TypeScript npm package supplies the logo, hero imagery, region list, locale messages, and tile-layer URLs. See [Frontend → Configuration](frontend.md#configuration).

The India and Paraguay deployments referenced above are working examples of all four pieces, end-to-end. You can clone either as a starting template.

## Keeping data fresh

Once the platform is live, refreshing data means **updating the input files and re-running the importers**:

```bash
docker exec context_layer_Backend python manage.py import_indicators
docker exec context_layer_Backend python manage.py import_data
```

`import_data` deletes existing rows for the affected geographies and time periods before reinserting, so it's safe to re-run for the same period after a correction. Most deployments run this on a monthly schedule via cron (or whatever scheduler their infrastructure provides) after their upstream risk-model pipeline produces a new CSV.

## Production deployment checklist

The platform is a stock Django + Next.js + PostgreSQL/PostGIS + Redis stack; a production setup follows the usual patterns for that stack. Things to confirm before going live:

- [ ] Set `DJANGO_ENV=production`, generate a real `SECRET_KEY`, and populate `ALLOWED_HOSTS` for the backend (see [Data Management → Production](data-management.md#production)).
- [ ] Set `NEXT_PUBLIC_DATA_MANAGEMENT_LAYER_URL` and `SITE_URL` on the frontend to your public hostnames (see [Frontend → Environment Variables](frontend.md#environment-variables)).
- [ ] Front the frontend and backend with a reverse proxy that terminates TLS (nginx, Caddy, Traefik, or a managed load balancer).
- [ ] Configure a backup strategy for the PostGIS database. `pg_dump` of the `postgres` database is sufficient for most deployments, since all data is reproducible from the source CSVs.
- [ ] Confirm Redis persistence settings match your cache-warmth requirements (the default in-memory mode is fine; data is re-cached on first request after eviction).
- [ ] (Optional) Wire up [Sentry](frontend.md#sentry) for runtime error reporting.
- [ ] (Optional) Wire up analytics and verification tokens via [environment variables](frontend.md#analytics).

## Privacy, accessibility, and security

- **Privacy**: The platform processes only **public administrative data**, no PII. Analytics (Google Analytics, Hotjar) are off by default; each requires an explicit environment-variable opt-in per deployment. The DataSpace integration, when enabled, can host published datasets but inherits whatever privacy posture that service is configured for.
- **Accessibility**: Built with accessible component primitives ([opub-ui](https://www.npmjs.com/package/opub-ui), [react-aria](https://react-spectrum.adobe.com/react-aria/)). Keyboard navigation and ARIA semantics are part of the component library's contract. Choropleth maps include a legend and offer a tabular view of the same data.
- **Security**: Report vulnerabilities to <info@civicdatalab.in>. Component secrets (database password, Django secret key, Sentry tokens) live in environment variables, never in `config.toml` or the branding package.
- **License**: All components are licensed under [GNU Affero General Public License v3 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.html). Each component repository includes its own `LICENSE` file. Deployments that customise the code and offer it as a service must make their modifications available under the same terms.

## Contributing

See [Contributing](contributing.md) for issue trackers and contact information, and [Development](development.md) for design notes for code contributors.
