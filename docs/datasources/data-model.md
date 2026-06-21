# Risk model

**Repository**: [risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic)

IDS-DRR aims to fill a need where authorities lack the data to make actionable insights when it comes to long-term disaster risk mitigation. The platform is based primarily on the UN's [SENDAI framework](https://www.undrr.org/implementing-sendai-framework/what-sendai-framework) for Disaster Risk Reduction (DRR). Within this framework, risk is defined as being proportional to the following factors:

| Factor | Definition | Example indicators |
|--------|------------|-------------------|
| **Exposure** | Number of people and assets exposed to a disaster event | Total Population, total households, cultivated crop area |
| **Hazard** | The geographical characteristics that contribute to the likelihood of a natural disaster | Inundation, rainfall, distance from river |
| **Vulnerability** | The socio economic factors that increase the risk due to a disaster event or determine a population's ability to recover from one | Access to infrastructure: roads, health centers, railways. Actual losses and damages due to disaster events |
| **Coping Capacity** | The ability of a population to respond to the disaster event and reduce its risk | Total disaster-related tenders awarded, restoration funds |

The relationship between these factors and risk can be defined as follows:

```text
Risk ∝ Exposure^a × Hazard^b × Vulnerability^c × (lack of coping capacity)^d
```

Where a, b, c and d are weightages currently provided to the different factor scores.

The data model for IDS-DRR was built keeping this relationship in mind, and collates a variety of different sources to model risk scores for each factor.

## Risk model overview

Each model run produces 4 factor scores (hazard, exposure, vulnerability, coping capacity) and a final risk score for each sub-district and district, per time period (deployments typically use a monthly cadence). All the scores range from 1-5, where 1 corresponds to lowest risk / hazard / vulnerability, and 5 corresponds to highest.

The model produces separate per-factor output files — by default `factor_scores_l1_hazard.csv`, `factor_scores_l1_exposure.csv`, `factor_scores_l1_vulnerability.csv`, and `factor_scores_l1_government-response.csv`, configurable in [scores_config.toml](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/disaster_risk_score_model/config_templates/scores_config.toml) — plus two TOPSIS outputs: `risk_score.csv` (sub-district rows only) and `risk_score_district.csv` (sub-district and district rows combined, ready for the platform's `import_data` step). The output schema is documented in full in [docs/data_dictionary.csv](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/docs/data_dictionary.csv) in the model repository.

For the inputs used by the Assam reference deployment for each factor below, see [Data sources](data-ingestion.md).

## Exposure

Exposure measures the population and value of assets at risk during a disaster event. Common indicators are total population and household count per sub-district per month; deployments may substitute or extend these with asset-value or infrastructure-exposure variables appropriate to their context.

### Factor score

To calculate the Exposure factor score for a particular month, the data for each indicator across all the sub-districts are normalized using MinMaxScaler in order to scale the range of values from 0-1. The individual feature scores are then added, and mean and standard deviation of the resulting "sum" column are then calculated. The factor score is then assigned to each sub-district based on z-score binning:

| Factor Cumulative Value | Factor Score |
|------------------------|--------------|
| `exposure['sum'] <= mean` | 1 |
| `exposure['sum'] > mean & <= mean + std` | 2 |
| `exposure['sum'] > mean + std & <= mean + 2*std` | 3 |
| `exposure['sum'] > mean + 2*std & <= mean + 3*std` | 4 |
| `exposure['sum'] > mean + 3*std` | 5 |

## Hazard

Hazard reflects the geographical and hydro-meteorological characteristics that contribute to the likelihood of a natural disaster resulting in loss of life or property. The specific indicators are hazard-dependent: a flood deployment might capture inundation extent, rainfall, and drainage; a drought deployment might substitute soil moisture, evapotranspiration, and precipitation deficit; an earthquake deployment might substitute seismic activity and proximity to faults.

### Factor score

To calculate the Hazard factor score for a particular month, the data for each indicator across all the sub-districts are normalized using MinMaxScaler. The mean and standard deviation for each feature is then calculated across all the sub-districts for the month. A score is then assigned to each feature based on the z-score binning method. To obtain the final hazard score, the arithmetic mean of the individual factor scores is taken and rounded to the nearest integer.

## Vulnerability

Vulnerability is a measure of the resilience of a population, and indicates the actual impact of the disaster event as experienced by the population. This resilience is influenced by socio-economic conditions, infrastructure facilities present, and the actual losses and damages due to disaster events. Indicators typically group into three categories:

- **Infrastructure**: facility counts and lengths (`schools_count`, `health_centres_count`, `rail_length`, `road_length`), and household-level service access (electricity, piped water, sanitation, net sown area).
- **Demographic**: indicators such as `mean_sexratio` and `sum_aged_population`.
- **Losses and damages**: reported impact — population affected, lives lost, crop area damaged, roads/bridges/embankments damaged. Typically sourced from the disaster management authority.

### Factor score

To calculate the Vulnerability factor score, a method known as **Data Envelopment Analysis (DEA)** is utilized. DEA calculates an "efficiency score" for each spatial unit based on its ability to minimize losses and damages given its available infrastructure and vulnerable population.

#### Pre-processing

Before the DEA model is run, select variables are normalised to make them comparable across units of different sizes:

- `population_affected_total` and `human_lives_lost` are divided by `total_population`
- `crop_area` is divided by `net_sown_area_ha`
- Road, bridge, and protective-infrastructure damage variables are divided by area (km²)
- Infrastructure density variables (`schools_count`, `health_centres_count`, `rail_length`, `road_length`, `elderly_population`) are also divided by area (km²)

#### Damage-weighted scoring

A composite damage score is computed to increase the sensitivity of the DEA during months when actual hazard damage occurred:

```text
damage_score = MinMax_sum(damage_vars) + 1
custom_weight = damage_score²
```

If any damage variable exceeds a threshold (0.0001), the damage variables and negative-polarity inputs are multiplied by `custom_weight`. This amplifies the signal in damaged units so that the DEA correctly penalises poor conditions that co-occur with high observed damage.

#### DEA transformations

The following transformations are made before running the DEA model:

1. All input and output variables are normalized using MinMaxScaler (0-1) within each month.
2. **Positive-resilience inputs** — indicators where a higher value means better resilience (e.g. `schools_count`, `health_centres_count`, `rail_length`, `road_length`, `electricity_access`) — are inverted (subtracted from 1) so that the DEA correctly treats their absence as a vulnerability.
3. The losses and damage output variables are all inverted (subtracted from 1), so that the DEA model seeks units that minimise damage as its "efficient" outcome.

The DEA model is then run using **PuLP with the open-source CBC solver** (Constant Returns to Scale, input-oriented). The efficiency scores output by the model are classified into 5 vulnerability classes using the **Fisher-Jenks Natural Breaks** algorithm, which minimises within-class variance. Classification is reversed: high efficiency maps to low vulnerability (class 1); low efficiency to high vulnerability (class 5).

## Coping capacity

Coping capacity is indicative of the resources available to a sub-district to respond to, or minimize the losses caused by, disaster events. The risk model expects financial-allocation indicators — typically tender awards and disaster-relief funds — geocoded to the sub-district and broken down by scheme or category, timestamped to the month.

### Factor score

For each indicator category, the cumulative sum of the values of tenders received in that financial year up to that point in time is calculated, and the range of values is normalized using MinMaxScaler. A final "government response" score is assigned using a modified z-score binning method (higher tender value = lower risk score):

| Factor Cumulative Value | Factor Score |
|------------------------|--------------|
| `response['sum'] <= mean` | 5 |
| `response['sum'] > mean & <= mean + std` | 4 |
| `response['sum'] > mean + std & <= mean + 2*std` | 3 |
| `response['sum'] > mean + 2*std & <= mean + 3*std` | 2 |
| `response['sum'] > mean + 3*std` | 1 |

## Final risk score

The final risk score is calculated for each sub-district using a multi-criteria decision making method called **TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution).

Before running the TOPSIS model, weights are assigned to each factor type based on its importance to the final risk score. The weightages are defined using the document "Disaster Risk and Resilience in India" drafted by the Ministry of Home Affairs and UNDP:

| Factor | Hazard | Exposure | Vulnerability | Coping Capacity |
|--------|--------|----------|---------------|-----------------|
| **Weightage** | 4 | 1 | 2 | 2 |

These weights are configured in `topsis_config.toml` and can be adjusted without editing any code, to reflect local context or policy priorities.

TOPSIS takes the individual factor scores and corresponding weightages as inputs. It works by defining an ideal solution and a non-ideal solution based on the factor scores, and computing the similarity of each sub-district's factor score matrix to the ideal and non-ideal solution. The final risk score is generated by binning TOPSIS output into categories from 1-5 based on their relative scores.

Once the TOPSIS score is calculated at the sub-district level, the factor scores and final risk score are calculated at the district level by grouping sub-districts within each month by their corresponding districts, and calculating the arithmetic mean of the sub-district scores for each factor.

## Limitations and responsible use

The following limitations should be considered when interpreting outputs from this model:

- **Scores are relative, not absolute.** All factor scores and the composite risk score are computed relative to other sub-districts within the same monthly dataset. A score of 1 (low risk) does not indicate absence of risk — it indicates lower risk than peers in that period.
- **The model is not a forecast.** It reflects observed conditions and historical data. It should not be used to predict future disaster events.
- **Data staleness.** Outputs are only as fresh as their inputs. Sources with infrequent updates (one-time surveys, terrain models, census-extrapolated population figures) can lag real conditions by years. Adopters should publish the vintage of each input alongside the scores; results in areas that have seen significant infrastructure or demographic change since the most recent update should be interpreted with caution. See [Data sources](data-ingestion.md) for the vintages used by the Assam reference deployment.
- **Low-risk classifications must not be used to justify withdrawing services.** A low vulnerability or risk score reflects relative conditions across the dataset; it does not mean a sub-district is safe or that services can be reduced.
- **DEA efficiency scores are sensitive to the composition of the peer group.** Adding or removing sub-districts from the dataset will change the efficiency frontier and therefore shift scores.

For full guidance on responsible use, see [RESPONSIBLE_DATA_USE.md](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/RESPONSIBLE_DATA_USE.md) in the model repository.
