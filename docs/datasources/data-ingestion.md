# Data sources

This page documents the data sources that feed the IDS-DRR [risk model](data-model.md). The scripts used to acquire, clean, and join these sources are maintained in the companion repository [CivicDataLab/flood-data-ecosystem-generic](https://github.com/CivicDataLab/flood-data-ecosystem-generic), which produces the `MASTER_VARIABLES.csv` file consumed by the modelling pipeline. The modelling layer itself is maintained in [CivicDataLab/risk-score-model-generic](https://github.com/CivicDataLab/risk-score-model-generic).

Each source's raw data is stored before processing to required formats:

1. **Data Classifier**: The raw datasets are then transformed into input variables for the statistical model. These input variables are calculated at the sub-district level (the lowest administrative unit imported for the deployment).
2. **Data Pipeline**: The data is processed through a series of steps (data pipeline) to be used by different components in the system.
3. **Data Update**: The updation of data is achieved by setting up data pipelines scheduled to run on different intervals based on the data source. Some pipelines update data on a near real time basis.

## Reference deployment: Assam, India

The tables below list the data sources used by the Assam (India) reference deployment. They are **illustrative** — other regions will use different sources appropriate to their context. The risk-model methodology itself is generic; only the inputs change.

In Assam, the sub-district level is the **revenue circle**, which is the unit of decision making for the Assam State Disaster Management Authority (ASDMA).

> **Note on Google Earth Engine (GEE):** Several hazard and exposure sources in the Assam deployment are accessed via GEE. For deployments requiring a fully open pipeline, the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) provides an open API for equivalent Sentinel imagery without a commercial dependency.

### Hazard variables

| Data Source | Data Variables | Frequency | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|------------------------|-----------------|
| [BHUVAN](https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php) | Inundation percentage, Inundation intensity | Monthly | Flood inundation images are accessed through BHUVAN's WMS server and images of each month are processed and aggregated | NRSC open data portal; Government Open Data Licenses (GODL)free for non-commercial use |
| [SENTINEL](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) | NDVI | Monthly | SENTINEL-2 MSI's images are accessed from Google Earth Engine (GEE) and then processed for each month. Open alternative: Copernicus Data Space Ecosystem API | Copernicus open access (CC-BY-4.0 equivalent) |
| [IMD](https://imdlib.readthedocs.io/en/latest/) | Rainfall | Monthly | Indian Meteorological Department (IMD) data is made available through a python package called [imd-lib](https://imdlib.readthedocs.io/en/latest/). The data is accessed in the form of daily rasters, which are processed for each month | IMD open data; Government Open Data Licenses (GODL) free for research and public use |
| [NASADEM](https://www.earthdata.nasa.gov/esds/competitive-programs/measures/nasadem) | Elevation, Slope | One-Time | Digital Elevation Model (DEM) is sourced from Google Earth Engine (GEE) in the form of a raster. Slope is calculated from the DEM using a mathematical expression. The rasters are processed to aggregate values for each revenue circle. Open alternative: Copernicus Data Space Ecosystem API | NASA Earthdata open access |
| [GCN250](https://gee-community-catalog.org/projects/gcn250/) | Surface runoff | One-Time | The Global Curve Numbers (GCN) dataset is available as a raster image on GEE Community Catalog. This raster is processed to calculate aggregate value for each revenue circle | CC-BY-4.0 |
| [WRIS](https://indiawris.gov.in/wris/) | Distance from rivers, Drainage density | One-Time | GIS data accessed from WRIS servers is processed to calculate the variables of interest for each revenue circle | Government of India open data; free for research and public use |

### Exposure variables

| Data Source | Data Variables | Frequency | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|------------------------|-----------------|
| [BHARAT MAPS](https://bharatmaps.gov.in/newversion/map.aspx) | Health centers per revenue circle, Road length per revenue circle, Rail length per revenue circle, School per revenue circle | One-Time | The GIS data from BHARAT MAPS data can be accessed through the ArcGIS REST server. This is a snapshot data that we can access through softwares like QGIS. After accessing the GIS data, we process it to calculate the variables of interest | Government Open Data License (GODL); free for research and public use |
| [World Pop](https://www.worldpop.org/) | Total Population | Yearly | Since the national census was delayed past 2011, World Pop's annual estimates are used. Raster files from 2016-2020 are clipped to the region of analysis and extrapolated using linear regression for 2021-24 | CC-BY-4.0 |
| [Mission Antyodaya 2022-23](https://missionantyodaya.dord.gov.in/getStateProgressView.html?stateCode=22) | Total Number of Households | One-Time | Mission Antyodaya contains socio-economic variables at the village level, processed to find aggregates for each sub-district. Rural household counts come directly from the dataset; urban household counts are extrapolated from urban population figures | Government of India open data; Government Open Data License (GODL) free for research and public use |

### Vulnerability variables

| Data Source | Data Variables | Frequency | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|------------------------|-----------------|
| [World Pop](https://www.worldpop.org/) | Sex-Ratio, Aged population (>=65), Children population (<=5) | Yearly | World Pop's estimates for every year to calculate population in each subdistrict | CC-BY-4.0 |
| [Mission Antyodaya 2022-23](https://missionantyodaya.dord.gov.in/getStateProgressView.html?stateCode=22) | Net sown area, Availability of domestic electricity, Availability of telephone services, Households with piped water connections, Households without sanitary latrines | One-Time | Mission Antyodaya 2022-23 contains data on socio-economic variables at the village level, data is processed to find aggregates for each subdistrict | Government of India open data; Government Open Data License (GODL) free for research and public use |

### Damage and losses

| Data Source | Data Variables | Frequency | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|------------------------|-----------------|
| [DRIMS](https://drims.veldev.com/) | Population affected, Crop area affected, Roads damaged, Bridges damaged, Embankments damaged, Human lives lost, Animals affected, Animals washed away, Erosion damages, Houses damaged | Monthly | ASDMA collects Flood damages datasets on a daily basis and makes it available in the form of FRIMS system. | ASDMA government data; shared under CC-BY 4.0 under data-sharing agreement with ASDMA |

### Government response

| Data Source | Data Variables | Frequency | Method of data sourcing | License / Terms |
|-------------|----------------|-----------|------------------------|-----------------|
| [TENDERS](https://assamtenders.gov.in/nicgep/app?page=WebTenderStatusLists&service=page) | Total number of flood related tenders awarded, Total awarded amount of tenders, Tenders - scheme wise (SDRF, SOPD, RIDF), Tenders works wise (Roads, Bridges, Embankments, Erosion), Tenders Type (Immediate measure, Repairs, Preparation, Goods) | Monthly | Awarded Tenders (AOC) are scraped for each month from the assam tenders website. The scraped data is then processed to calculate flood related tenders. Each tender is geotagged to a revenue circle to calculate the variables for each revenue circle | Government of India open procurement data (GePNiC); Government Open Data License (GODL) |
| State Disaster Relief Funds | Sanctioned funds for flood preparedness and response | Yearly | Funds sanctioned by the state to districts, manually scraped from the annual State Executive Committee (SEC) meeting minutes | Public government records |

