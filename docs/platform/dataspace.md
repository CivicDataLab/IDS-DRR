# DataSpace Integration

[DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) is a separate CivicDataLab service that provides a datasets catalog, search, publishing, and chart generation. It is **optional**: the core IDS-DRR platform (analytics maps, risk scores, indicators, reports) works without it. When configured, it powers the frontend's `/datasets` routes and the PDF report's dynamic charts.

This page covers the integration points. Setup of DataSpace itself is documented in its own [repository](https://github.com/CivicDataLab/DataSpaceBackend).

## What DataSpace provides

| Frontend feature | DataSpace endpoint | Consumed by |
|---|---|---|
| Dataset catalog, search | `/api/graphql` (datasets, search queries) | `app/[locale]/datasets/**` |
| Chart visualisations on a dataset detail page | `/api/graphql` (`CHARTS_QUERY`) | `Details` component |
| Map charts (GeoJSON geometry) | `/api/graphql` returns `chartType`; the data-management backend's `/chart-types/<chart_type>` returns the GeoJSON | `MapChart` component |
| PDF report dynamic charts | `/api/generate-dynamic-chart/` | `ids-drr-plugin` package (when `reports_enabled`) |

## Frontend environment variables

Point the frontend at your DataSpace instance via `.env.local` (see [Frontend](frontend.md#environment-variables)):

```env
BACKEND_URL="https://api.dataspace.example.in"
NEXT_PUBLIC_BACKEND_URL="https://api.dataspace.example.in"
```

Unset both to disable DataSpace-dependent features. The catalog routes still render but return empty lists.

## How chart rendering works

Each dataset's detail page runs `CHARTS_QUERY` against DataSpace:

```graphql
query chartsData($datasetId: UUID!) {
  chartsDetails(datasetId: $datasetId) {
    id
    name
    description
    chartType      # deployment-chosen string, e.g. "ASSAM_DISTRICT", "MULTILINE"
    chart          # a complete echarts option object
  }
}
```

For non-map charts the `chart` option is rendered directly by `ReactECharts`. For map charts (those whose `chart.series[*].type === 'map'`), the frontend additionally fetches the map's geometry from the data-management backend and registers it with echarts by the `chartType` name.

The frontend doesn't know which geographies a `chartType` refers to. Mapping `chartType` → geographies lives on the data-management side.

## Adding a new map chart

Prerequisites: a dataset in DataSpace that produces a chart option with `series.type === 'map'` and a `chartType` identifier you choose (e.g. `BIHAR_DISTRICT`).

**1. Configure the data-management backend.** Add an entry to `[[chart_types]]` in the backend `config.toml`:

```toml
[[chart_types]]
chart_type = "BIHAR_DISTRICT"
state = "Bihar"
geo_type = "DISTRICT"
```

- `chart_type` must match exactly what DataSpace returns in `chartsDetails.chartType` (the frontend lowercases it before fetching).
- `state` is matched case-insensitively against `Geography.name` of the parent (or grandparent) row.
- `geo_type` matches `Geography.type` — typical values are `STATE`, `DISTRICT`, `REVENUE CIRCLE`, etc.

**2. Ensure the geographies have geometry.** The endpoint serves `Geography.simple_geom` (a simplified copy of `geom`, created at import time per the `simplify_tolerance` config). If `simple_geom` is null for the matched rows, they're omitted from the FeatureCollection.

`Geography.name` is what ends up in each feature's `properties.name` (uppercased). echarts matches your chart's `series.data[*].name` against these; the chart option produced by DataSpace must use the same casing convention.

**3. Verify the endpoint.**

```bash
curl http://localhost:8000/chart-types/bihar_district | jq '.features | length'
```

Expect a non-zero count. A 404 means the `chart_type` isn't in `[[chart_types]]`; an empty `features` array means the filter matched no rows with a non-null `simple_geom`.

**4. No frontend change needed.** As long as the DataSpace chart option has `series.type === 'map'` and its `series.map` name matches `chartType.toLowerCase()`, the existing `MapChart` component picks it up.

## Related configuration

- [Frontend environment variables](frontend.md#environment-variables) — `BACKEND_URL`, `NEXT_PUBLIC_BACKEND_URL`.
- [Data Management API deployment configuration](data-management.md#deployment-configuration) — `[[chart_types]]` and `simplify_tolerance` live in `config.toml`. See [`config.toml.example`](https://github.com/CivicDataLab/IDS-DRR-Data-Management/blob/dev/config.toml.example) for the annotated reference.
- [PDF report opt-in](data-management.md#pdf-report-opt-in) — the report package uses DataSpace's `/api/generate-dynamic-chart/` via `CHART_API_BASE_URL`.
