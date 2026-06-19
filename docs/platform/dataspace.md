# DataSpace Integration

[DataSpaceBackend](https://github.com/CivicDataLab/DataSpaceBackend) is a separate CivicDataLab service that provides a datasets catalog, search, publishing, and chart generation. It is **optional**: the core IDS-DRR platform (analytics maps, risk scores, indicators) works without it. When configured, it powers the analytics page's chart view and the datasets catalog.

This page covers the integration points. Setup of DataSpace is documented in its own [repository](https://github.com/CivicDataLab/DataSpaceBackend).

## Features

| Frontend feature | DataSpace endpoint | Consumed by |
|---|---|---|
| Analytics page chart view | `/api/generate-dynamic-chart/<state-resource-id>` | `ChartView` component |
| Dataset catalog and search | `/api/graphql` (dataset listing and search queries) | `app/[locale]/datasets/**` |
| Charts on dataset detail pages | `/api/graphql` | `Details` component |
| Maps on dataset detail pages | `/api/graphql` returns `chartType`, and the Data Management API's `/chart-types/<chart_type>` returns the GeoJSON | `MapChart` component |

## Frontend environment variables

Point the frontend at your DataSpace instance via `.env.local` (see [Frontend](frontend.md#environment-variables)):

```ini
BACKEND_URL="https://api.dataspace.example.in"
NEXT_PUBLIC_BACKEND_URL="https://api.dataspace.example.in"
```

Unset both to disable DataSpace-dependent features. The `/datasets` routes return 404, and the analytics page's chart-view tab is not rendered.

## How chart rendering works

Each dataset's detail page runs this query against DataSpace:

```graphql
query chartsData($datasetId: UUID!) {
  chartsDetails(datasetId: $datasetId) {
    id
    name
    description
    chartType   # deployment-chosen string, e.g. "ASSAM_DISTRICT", "MULTILINE"
    chart       # a complete echarts option object
  }
}
```

For non-map charts, the `chart` option is rendered directly by `ReactECharts`. For map charts (those whose `chart.series[*].type === 'map'`), the frontend additionally fetches the map's geometry from the Data Management API and registers it with echarts by the `chartType` name.

The frontend doesn't know which geographies a `chartType` refers to. Mapping `chartType` → geographies lives in the Data Management API's configuration.

## Adding a new map chart

Prerequisite: A dataset in DataSpace that produces a chart option with `series.type === 'map'` and a `chartType` identifier you choose (e.g. `BIHAR_DISTRICT`).

**1. Configure the Data Management API.** Add an entry to `[[chart_types]]` in its `config.toml`:

```toml
[[chart_types]]
chart_type = "BIHAR_DISTRICT"
state = "Bihar"
geo_type = "DISTRICT"
```

- `chart_type` must match exactly what DataSpace returns in `chartsDetails.chartType`.
- `state` is matched case-insensitively against `Geography.name` of the parent (or grandparent) row.
- `geo_type` matches `Geography.type` – a value in one of your `[[geojson]]` entries' `geo_type`.

**2. Ensure the geographies have geometries.** The endpoint serves `Geography.simple_geom` (a simplified copy of `geom`, created at import time per the `simplify_tolerance` config). If `simple_geom` is null for the matched rows, they're omitted from the FeatureCollection.

`Geography.name` is what ends up in each feature's `properties.name`, uppercased. echarts matches your chart's `series.data[*].name` against these, so the chart option produced by DataSpace must use uppercased names, too.

**3. Verify the Data Management API's endpoint.** In development, for example:

```bash
curl http://localhost:8000/chart-types/BIHAR_DISTRICT | jq '.features | length'
```

Expect a non-zero count. A 404 means the `chart_type` isn't in `[[chart_types]]`; an empty `features` array means the filter matched no rows with a non-null `simple_geom`.

No frontend change is needed: the existing `MapChart` component picks the chart up automatically.

## Related configuration

- [Frontend environment variables](frontend.md#environment-variables): `BACKEND_URL`, `NEXT_PUBLIC_BACKEND_URL`.
- [Data Management API configuration](data-management.md#configuration): `[[chart_types]]` and `simplify_tolerance` live in `config.toml`. See [config.toml.example](https://github.com/CivicDataLab/IDS-DRR-Data-Management/blob/dev/config.toml.example) for the annotated reference.
