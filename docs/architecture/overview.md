# Architecture overview

IDS-DRR's end-to-end flow spans data sourcing, risk modelling, the platform itself, and (optionally) publishing.

## Data flow

1. **Identify**: Determine the required data, sources, and variables.
2. **Collect**: Gather raw data via APIs, satellite imagery, and government portals.
3. **Process**: Clean, transform, and standardize raw inputs into per-region indicator CSVs.
4. **Model**: Run the [risk-score model](https://github.com/CivicDataLab/risk-score-model-generic) over those CSVs to produce per-administrative-unit factor scores. See [Risk-scoring methodology](../datasources/data-model.md).
5. **Analyze**: The [Data Management API](../platform/data-management.md) ingests the model outputs and serves them via GraphQL.
6. **Front-end**: The [Frontend](../platform/frontend.md) renders interactive maps, dashboards, and reports.
7. **Publish** *(optional)*: The [DataSpace Backend](../platform/dataspace.md) hosts a dataset catalog and chart-generation API.
8. **List** *(optional)*: The frontend's `/datasets` routes browse and search that catalog.

![data flow](https://github.com/CivicDataLab/IDS-DRR/assets/39596102/2b0d1356-e6d8-4676-a9ba-0f31eaca18c5)

Stages 1–4 sit upstream of this repository (see [data sources](../datasources/data-ingestion.md) and the [risk-score model](https://github.com/CivicDataLab/risk-score-model-generic)). Stages 5–6 are the core platform documented under [Platform technical documentation](../platform/index.md). Stages 7–8 are opt-in.
