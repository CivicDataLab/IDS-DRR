# Data Model

## Relevance to the Sustainable Development Goals

The IDS-DRR platform directly supports:

- **SDG 13 — Climate Action**, in particular target 13.1 (strengthen resilience and adaptive capacity to climate-related hazards) and indicator 13.1.1 (number of people affected by disasters).
- **SDG 11 — Sustainable Cities and Communities**, in particular target 11.5 (reduce deaths and economic losses caused by disasters) and target 11.b (integrated policies for resilience to disasters).

By producing transparent, reproducible risk scores at granular administrative levels, the platform enables agencies to plan mitigation, target relief, and audit historical response patterns against measured exposure and vulnerability.

## Context

The IDS-DRR platform aims to fill a need where authorities lack the data to make actionable insights when it comes to long term flood risk mitigation. The platform is designed based primarily on the UN's SENDAI framework for Disaster Risk Reduction (DRR). Within this framework, flood risk is defined as being proportional to the following factors:

| Factor | Definition | Example indicators |
|--------|------------|-------------------|
| **Exposure** | Number of people and assets exposed to a disaster event | Total Population, total households, cultivated crop area |
| **Hazard** | The geographical characteristics that contribute to the likelihood of a natural disaster | Inundation, rainfall, distance from river |
| **Vulnerability** | The socio economic factors that increase the risk due to a disaster event or determine a population's ability to recover from one | Access to infrastructure: roads, health centers, railways. Actual losses and damages due to disaster events |
| **Coping Capacity** | The ability of a population to respond to the disaster event and reduce its risk | Total Flood Tenders received, Restoration funds |

The relationship between these factors and flood risk can be defined as follows:

```text
Risk ∝ Exposure^a × Hazard^b × Vulnerability^c × (lack of coping capacity)^d
```

Where a, b, c and d are weightages currently provided to the different factor scores.

The data model for the IDS-DRR platform was built keeping this relationship in mind, and collates a variety of different sources to model risk scores for each factor.

## Data Model Overview

The data model is run monthly and outputs 5 factor scores and a risk score for each revenue circle and district. All the scores range from 1-5, where 1 corresponds to lowest risk / hazard / vulnerability, and 5 corresponds to highest.

The model produces separate per-factor output files (`factor_scores_l1_flood-hazard.csv`, `factor_scores_l1_exposure.csv`, `factor_scores_l1_vulnerability.csv`, `factor_scores_l1_government-response.csv`) and a final platform-ready output (`risk_score_district.csv`) containing both block-level and district-level rows. The output schema is documented in full in [`docs/data_dictionary.csv`](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/docs/data_dictionary.csv) in the model repository.

## Exposure

Exposure indicates the total population and value of assets that is at risk during a disaster event. In IDS-DRR, this consists of the two indicators: `total_households` taken from Mission Antyodaya, and `Sum_population`, derived from UN WorldPOP.

### Transformation of each indicator

- **Sum_population**: As the Census figures have not been updated since 2011, population figures have been estimated using UN WorldPOP's population dataset. Raster files from 2016-2020 are clipped to the region of analysis, and extrapolated using linear regression for 2021-24.
- **Total_households**: Household figures for rural settlements are available in the Mission Antyodaya dataset. Figures for urban settlements are extrapolated from urban population figures.

### Exposure Factor Score

To calculate the Exposure factor score for a particular month, the data for each indicator across all the revenue circle / tehsils are normalized using Min-max Scaler in order to scale the range of values from 0-1. The individual feature scores are then added, and mean and standard deviation of the resulting "sum" column are then calculated. The factor score is then assigned to each revenue circle based on z-score binning:

| Factor Cumulative Value | Factor Score |
|------------------------|--------------|
| `exposure['sum'] <= mean` | 1 |
| `exposure['sum'] > mean & <= mean + std` | 2 |
| `exposure['sum'] > mean + std & <= mean + 2*std` | 3 |
| `exposure['sum'] > mean + 2*std & <= mean + 3*std` | 4 |
| `exposure['sum'] > mean + 3*std` | 5 |

## Hazard

Hazard is defined by the geographical and hydro-meteorological characteristics that contribute to the likelihood of a natural disaster resulting in loss of life or property. It consists of the following datasets:

- **Drainage Density**: A measure of how many rivers/streams are present in an area, derived from the Digital Elevation Model (DEM), extracted from NASADEM's SRTM dataset. Only needs to be sourced once.
- **Rainfall**: Daily rainfall figures are scraped from IMD using the IMDlib library, and transformed to extract `mean_rain` (average rainfall across a month) and `max_rain` (highest single instance of recorded daily rainfall).
- **Inundation**: When available, inundation data is taken from Bhuvan's flood database. The data comes in the form of raster images where each pixel corresponds to a 10m × 10m area. These images are scraped and transformed to obtain `inundation_percentage` and `inundation_intensity`. In some cases, raster images are obtained from SENTINEL SAR-1 satellite imagery.

### Hazard Factor Score

To calculate the Hazard factor score for a particular month, the data for each indicator across all the revenue circle / tehsils are normalized using minmaxscaler. The mean and standard deviation for each feature is then calculated across all the revenue circles for the month. A score is then assigned to each feature based on the z-score binning method. To obtain the final hazard score, the arithmetic mean of the individual factor scores is taken and rounded to the nearest integer.

## Vulnerability

Vulnerability is a measure of the resilience of a population, and indicates the actual impact of flood as experienced by the population. This resilience is influenced by the socio-economic conditions, infrastructure facilities present and the actual losses and damages due to disaster events.

### Vulnerability Data Sources

- **Infrastructure**: For the indicators `schools_count`, `health_centres_count`, `rail_length`, and `road_length`, data is extracted from BharatMaps ArcGIS REST Server. Other infrastructure indicators are derived from the Mission Antyodaya dataset including: `Net sown area in hectares`, `average daily electricity availability in hours`, `Percentage of households without sanitation facilities` and `Percentage of households with piped water facilities`.
- **Demographic**: Indicators include `mean_sexratio` and `sum_aged_population`, estimated using the UN WorldPOP's population dataset.
- **Losses and Damages**: All losses and damages indicators are received directly from the State Disaster Management Authorities. In the case of Assam, this data is scraped from DRIMS reports.

### Vulnerability Factor Score

To calculate the Vulnerability factor score, a method known as **Data Envelopment Analysis (DEA)** is utilized. DEA calculates an "efficiency score" for each spatial unit based on its ability to minimize losses and damages given its available infrastructure and vulnerable population.

#### Pre-processing

Before the DEA model is run, select variables are normalised to make them comparable across units of different sizes:

- `population_affected_total` and `human_lives_lost` are divided by `total_population`
- `crop_area` is divided by `net_sown_area_ha`
- Road, bridge, and flood protection damage variables are divided by area (km²)
- Infrastructure density variables (`schools_count`, `health_centres_count`, `rail_length`, `road_length`, `elderly_population`) are also divided by area (km²)

#### Damage-weighted scoring

A composite damage score is computed to increase the sensitivity of the DEA during months when actual flood damage occurred:

```text
damage_score = MinMax_sum(damage_vars) + 1
custom_weight = damage_score²
```

If any damage variable exceeds a threshold (0.0001), the damage variables and negative-polarity inputs are multiplied by `custom_weight`. This amplifies the signal in damaged units so that the DEA correctly penalises poor conditions that co-occur with high observed damage.

#### DEA transformations

The following transformations are made before running the DEA model:

1. All input and output variables are normalized using MinMaxScaler (0-1) within each month.
2. **Positive-resilience inputs** — indicators where a higher value means better resilience (e.g. `schools_count`, `health_centres_count`, `rail_length`, `road_length`, `electricity_access`, `piped_water_households_pct`) — are inverted (subtracted from 1) so that the DEA correctly treats their absence as a vulnerability.
3. The losses and damage output variables are all inverted (subtracted from 1), so that the DEA model seeks units that minimise damage as its "efficient" outcome.

The DEA model is then run using **PuLP with the open-source CBC solver** (Constant Returns to Scale, input-oriented). The efficiency scores output by the model are classified into 5 vulnerability classes using the **Fisher-Jenks Natural Breaks** algorithm, which minimises within-class variance. Classification is reversed — high efficiency maps to low vulnerability (class 1); low efficiency maps to high vulnerability (class 5).

## Coping Capacity / Government Response

Coping Capacity is indicative of the resources available to a revenue circle / tehsil to be able to respond to, or minimize the losses caused due to flood events.

### Data Sources

- **E-tenders**: Tenders scraped from each state's GEPNiC platform. The scraped tenders are analyzed and classified into different categories depending on tender sources and usage, and geocoded to the relevant district / revenue circle. Indicators include: `total_tender_awarded_value`, `SOPD_tenders_awarded_value`, `SDRF_tenders_awarded_value`, `RIDF_tenders_awarded_value`, `LTIF_tenders_awarded_value`, `CIDF_tenders_awarded_value`, `Preparedness Measures_tenders_awarded_value`, `Immediate Measures_tenders_awarded_value` and `Others_tenders_awarded_value`.
- **State Disaster Relief Funds**: Funds sanctioned by the state to districts for various flood preparedness and response measures, manually scraped from the annual SEC meeting minutes.

### Coping Capacity Factor Score

For each indicator category, the cumulative sum of the values of tenders received in that financial year up to that point in time is calculated, and the range of values is normalized using min-max scaler. A final "government response" score is assigned using a modified z-score binning method (higher tender value = lower risk score):

| Factor Cumulative Value | Factor Score |
|------------------------|--------------|
| `response['sum'] <= mean` | 5 |
| `response['sum'] > mean & <= mean + std` | 4 |
| `response['sum'] > mean + std & <= mean + 2*std` | 3 |
| `response['sum'] > mean + 2*std & <= mean + 3*std` | 2 |
| `response['sum'] > mean + 3*std` | 1 |

## Final Flood Risk Score

The final flood risk score is calculated for each revenue circle / tehsil using a multi-criteria decision making method called **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution).

Before running the TOPSIS model, weights are assigned to each factor type based on its importance to the final risk score. The weightages are defined using the document "Disaster Risk and Resilience in India" drafted by the Ministry of Home Affairs and UNDP:

| Factor | Hazard | Exposure | Vulnerability | Coping Capacity |
|--------|--------|----------|---------------|-----------------|
| **Weightage** | 4 | 1 | 2 | 2 |

These weights are configured in `topsis_config.toml` and can be adjusted without editing any code, to reflect local context or policy priorities.

TOPSIS takes the individual factor scores and corresponding weightages as inputs. It works by defining an ideal solution and a non-ideal solution based on the factor scores, and computing the similarity of each individual RC's factor score matrix to the ideal and non-ideal solution. The final risk score is generated by binning TOPSIS output into categories from 1-5 based on their relative scores.

Once the TOPSIS score is calculated at a revenue circle / tehsil level, the factor scores and final risk score are calculated at the district level by grouping revenue circles within each month by their corresponding districts, and calculating the arithmetic mean of the revenue circle scores for each factor.

The model produces per-factor output files and a final platform-ready file (`risk_score_district.csv`) containing both block-level and district-level rows. The complete output schema is documented in [`docs/data_dictionary.csv`](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/docs/data_dictionary.csv).

## Limitations and Responsible Use

The following limitations should be considered when interpreting outputs from this model:

- **Scores are relative, not absolute.** All factor scores and the composite risk score are computed relative to other revenue circles within the same monthly dataset. A score of 1 (low risk) does not indicate absence of risk — it indicates lower risk than peers in that period.
- **The model is not a forecast.** It reflects observed conditions and historical data. It should not be used to predict future flood events.
- **Data staleness.** Some inputs have not been updated recently: Mission Antyodaya figures are from 2020, NASADEM elevation data is from 2000, and national census-based figures have been extrapolated using WorldPop estimates since the 2011 census. Results in areas that have seen significant infrastructure or demographic change should be interpreted with caution.
- **Low-risk classifications must not be used to justify withdrawing services.** A low vulnerability or risk score reflects relative conditions across the dataset; it does not mean a revenue circle is safe or that services can be reduced.
- **DEA efficiency scores are sensitive to the composition of the peer group.** Adding or removing revenue circles from the dataset will change the efficiency frontier and therefore shift scores.

For full guidance on responsible use, see [`RESPONSIBLE_DATA_USE.md`](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/RESPONSIBLE_DATA_USE.md) in the model repository.

## License

The risk score model source code is licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/LICENSE). Sample and derived datasets produced by the model are released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/), unless a more restrictive licence applies to a specific upstream source, in which case the upstream licence governs that file.

## DPG Compliance

This project is submitted as a Digital Public Good. A full self-assessment mapping the project to all nine indicators of the [DPG Standard](https://digitalpublicgoods.net/standard/) is available in [`docs/dpg.md`](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/docs/dpg.md) in the model repository.