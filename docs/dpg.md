# Digital Public Goods Standard — Compliance Notes

This document maps the project to the nine indicators of the
[Digital Public Goods (DPG) Standard](https://digitalpublicgoods.net/standard/).
It is a self-assessment intended to support a DPG submission and to help
reviewers locate the relevant evidence in this repository.

| # | Indicator | Status | Evidence |
|---|-----------|--------|----------|
| 1 | **Relevance to SDGs** | ✅ | Supports SDG 13 (Climate Action, targets 13.1 / 13.1.1) and SDG 11 (Sustainable Cities, targets 11.5 / 11.b). See the *Relevance to the Sustainable Development Goals* section of [`README.md`](../README.md). |
| 2 | **Use of approved open licenses** | ✅ | Source code under **GNU AGPL-3.0** ([`LICENSE`](../LICENSE)); sample/derived data under **CC-BY-4.0**. The DEA module uses the open-source PuLP/CBC solver, not the proprietary Gurobi (see header of [`disaster_risk_score_model/dea.py`](../disaster_risk_score_model/dea.py)). |
| 3 | **Clear ownership** | ✅ | Owned by CivicDataLab; ownership and citation recorded in [`CITATION.cff`](../CITATION.cff) and the repository's GitHub organisation. |
| 4 | **Platform independence** | ✅ | Pure-Python package (3.11+) with only OSI-approved open-source dependencies (declared in [`pyproject.toml`](../pyproject.toml)). No mandatory proprietary components or hosted services. |
| 5 | **Documentation** | ✅ | End-user and adopter docs in [`docs/`](.) (getting-started, per-factor methodology, TOPSIS); contributor docs in [`CONTRIBUTING.md`](../CONTRIBUTING.md); a runnable reference example in [`contrib/india/example/`](../contrib/india/example/). |
| 6 | **Mechanism for extracting data** | ✅ | All inputs and outputs are non-proprietary, machine-readable formats — CSV (UTF-8), GeoJSON (EPSG:4326), TOML, Markdown. Output schema is described in [`docs/data_dictionary.csv`](./data_dictionary.csv). |
| 7 | **Adherence to privacy & applicable laws** | ✅ | Operates only on administrative-unit aggregates; processes no PII. See [`SECURITY.md`](../SECURITY.md) and [`RESPONSIBLE_DATA_USE.md`](../RESPONSIBLE_DATA_USE.md), which also note jurisdiction-specific obligations (e.g. India's DPDP Act 2023). |
| 8 | **Adherence to standards & best practices** | ✅ | Configuration-driven (no code edits needed to re-target a geography); automated tests under [`tests/`](../tests/) run in CI via [`.github/workflows/ci.yml`](../.github/workflows/ci.yml); open governance docs ([`CONTRIBUTING.md`](../CONTRIBUTING.md), [`CODE_OF_CONDUCT.md`](../CODE_OF_CONDUCT.md)); aligned with the Sendai Framework for DRR; supports OCDS-format procurement input. |
| 9 | **Do no harm by design** | ✅ | [`RESPONSIBLE_DATA_USE.md`](../RESPONSIBLE_DATA_USE.md) documents limitations (relative not absolute scores; not a forecast; low-risk classes must not justify withdrawing services). Aggregate-only processing avoids individual targeting. A private vulnerability-disclosure process is defined in [`SECURITY.md`](../SECURITY.md). |

## Notes for reviewers

- **Geography neutrality.** The core library (`disaster_risk_score_model/`,
  including its bundled config templates) is geography-neutral and runs out of
  the box on a synthetic sample. All India-specific assumptions (government
  finance schemes, fiscal calendar, administrative coding, named data sources)
  are isolated under [`contrib/india/`](../contrib/india/).
- **Reproducibility.** The sample dataset is generated deterministically by
  `drsm generate-sample-data` (module
  [`disaster_risk_score_model.sample_data`](../disaster_risk_score_model/sample_data.py));
  the full pipeline can be reproduced end-to-end from a fresh clone.
