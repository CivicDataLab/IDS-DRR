# Data Ingestion

This page documents the data sources that feed the IDS-DRR risk score model. The scripts used to acquire, clean, and join these sources are maintained in the companion repository [CivicDataLab/flood-data-ecosystem-generic](https://github.com/CivicDataLab/flood-data-ecosystem-generic), which produces the `MASTER_VARIABLES.csv` file consumed by the modelling pipeline. The modelling layer itself is maintained in [CivicDataLab/risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic).

Datasets are sourced from different sources before being consumed by the platform or the statistical models. Each source's raw data is stored before processing to required formats.

1. **Data Classifier**: The raw datasets are then transformed into input variables for the statistical model. These input variables are calculated at the revenue circle level.
2. **Data Pipeline**: The data is processed through a series of steps (data pipeline) to be used by different components in the system.
3. **Data Update**: The updation of data is achieved by setting up data pipelines scheduled to run on different intervals based on the data source. Some pipelines update data on a near real time basis.

## Data Sources

For the context of this project, we are sourcing data variables from the following data sources to understand flood hazard, exposure, vulnerability, damage & losses and government response.

Each variable is aggregated at the revenue circle level, which is the unit of decision making for the ASDMA.

> **Note on Google Earth Engine (GEE):** Several hazard and exposure sources in the Assam deployment are accessed via GEE. For deployments requiring a fully open pipeline, the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) provides an open API for equivalent Sentinel imagery without a commercial dependency.

### Hazard Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|--------------|------------------------|-----------------|
| [BHUVAN](https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php) | Inundation percentage, Inundation intensity | Monthly | 2024-08 | Flood inundation images are accessed through BHUVAN's WMS server and images of each month are processed and aggregated | NRSC open data portal; Government Open Data Licenses (GODL)free for non-commercial use |
| [SENTINEL](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) | NDVI | Monthly | 2024-09 | SENTINEL-2 MSI's images are accessed from Google Earth Engine (GEE) and then processed for each month. Open alternative: Copernicus Data Space Ecosystem API | Copernicus open access (CC-BY-4.0 equivalent) |
| [IMD](https://imdlib.readthedocs.io/en/latest/) | Rainfall | Monthly | Sep 2024 | Indian Meteorological Department (IMD) data is made available through a python package called [imd-lib](https://imdlib.readthedocs.io/en/latest/). The data is accessed in the form of daily rasters, which are processed for each month | IMD open data; Government Open Data Licenses (GODL) free for research and public use |
| [NASADEM](https://www.earthdata.nasa.gov/esds/competitive-programs/measures/nasadem) | Elevation, Slope | One-Time | 2000 | Digital Elevation Model (DEM) is sourced from Google Earth Engine (GEE) in the form of a raster. Slope is calculated from the DEM using a mathematical expression. The rasters are processed to aggregate values for each revenue circle. Open alternative: Copernicus Data Space Ecosystem API | NASA Earthdata open access |
| [GCN250](https://gee-community-catalog.org/projects/gcn250/) | Surface runoff | One-Time | 2019 | The Global Curve Numbers (GCN) dataset is available as a raster image on GEE Community Catalog. This raster is processed to calculate aggregate value for each revenue circle | CC-BY-4.0 |
| [WRIS](https://indiawris.gov.in/wris/) | Distance from rivers, Drainage density | One-Time | 2022 | GIS data accessed from WRIS servers is processed to calculate the variables of interest for each revenue circle | Government of India open data; free for research and public use |

### Exposure Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|--------------|------------------------|-----------------|
| [BHARAT MAPS](https://bharatmaps.gov.in/newversion/map.aspx) | Health centers per revenue circle, Road length per revenue circle, Rail length per revenue circle, School per revenue circle | One-Time | 2023-09 | The GIS data from BHARAT MAPS data can be accessed through the ArcGIS REST server. This is a snapshot data that we can access through softwares like QGIS. After accessing the GIS data, we process it to calculate the variables of interest | Government Open Data License (GODL); free for research and public use |
| [World Pop](https://www.worldpop.org/) | Total Population | Yearly | 2024 | Since the national census got delayed we are using World Pop's estimates for every year to calculate population in each revenue circle | CC-BY-4.0 |
| [Mission Antyodaya 2022-23](https://missionantyodaya.dord.gov.in/getStateProgressView.html?stateCode=22) | Total Number of Households | One-Time | 2020 | Mission Antyodaya 2022-23 contains data on socio-economic variables at the village level, data is processed to find aggregates for each subdistrict | Government of India open data; Government Open Data License (GODL) free for research and public use |

### Vulnerability Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|--------------|------------------------|-----------------|
| [World Pop](https://www.worldpop.org/) | Sex-Ratio, Aged population (>=65), Children population (<=5) | Yearly | 2024 | World Pop's estimates for every year to calculate population in each subdistrict | CC-BY-4.0 |
| [Mission Antyodaya 2022-23](https://missionantyodaya.dord.gov.in/getStateProgressView.html?stateCode=22) | Net sown area, Availability of domestic electricity, Availability of telephone services, Households with piped water connections, Households without sanitary latrines | One-Time | 2020 |Mission Antyodaya 2022-23 contains data on socio-economic variables at the village level, data is processed to find aggregates for each subdistrict | Government of India open data; Government Open Data License (GODL) free for research and public use |

### Damage and Losses

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|--------------|------------------------|-----------------|
| [DRIMS](https://drims.veldev.com/) | Population affected, Crop area affected, Roads damaged, Bridges damaged, Embankments damaged, Human lives lost, Animals affected, Animals washed away, Erosion damages, Houses damaged | Monthly | 09-2024 | ASDMA collects Flood damages datasets on a daily basis and makes it available in the form of FRIMS system. | ASDMA government data; shared under CC-BY 4.0 under data-sharing agreement with ASDMA |

### Government Response

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|--------------|------------------------|-----------------|
| [TENDERS](https://assamtenders.gov.in/nicgep/app?page=WebTenderStatusLists&service=page) | Total number of flood related tenders awarded, Total awarded amount of tenders, Tenders - scheme wise (SDRF, SOPD, RIDF), Tenders works wise (Roads, Bridges, Embankments, Erosion), Tenders Type (Immediate measure, Repairs, Preparation, Goods) | Monthly | 09-2024 | Awarded Tenders (AOC) are scraped for each month from the assam tenders website. The scraped data is then processed to calculate flood related tenders. We then geotag each of the flood related tender to a revenue circle to calculate the variables for each revenue circle | Government of India open procurement data (GePNiC); Government Open Data License (GODL) |

## License

The risk score model source code is licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://github.com/CivicDataLab/risk-score-model-generic/blob/main/LICENSE). Sample and derived datasets produced by the model are released under [Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/), unless a more restrictive licence applies to a specific upstream source, in which case the upstream licence governs that file.