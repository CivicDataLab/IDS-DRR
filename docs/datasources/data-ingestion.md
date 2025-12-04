# Data Ingestion

Datasets are sourced from different sources before consumed for the platform or the statistical models. Each source's raw data is stored before processing to required formats.

1. **Data Classifier**: The raw datasets are then transformed into input variables for the statistical model. These input variables are calculated at the revenue circle level.
2. **Data Pipeline**: The data is processed through a series of steps (data pipeline) to be used by different components in the system. For Data pipeline and orchestration, we use RabbitMQ and Prefect.
3. **Data Update**: The updation of data is achieved by setting up data pipelines scheduled to run on different intervals based on the data source. Some pipelines update data on a near real time basis.

## Data Sources

For the context of this project, we are sourcing data variables from the following data sources to understand flood hazard, exposure, vulnerability, damage & losses and government response.

Each variable is aggregated at the revenue circle level, which is the unit of decision making for the ASDMA.

### Hazard Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing |
|-------------|----------------|-----------|--------------|------------------------|
| [BHUVAN](https://bhuvan-app1.nrsc.gov.in/disaster/disaster.php) | Inundation percentage, Inundation intensity | Monthly | 2024-08 | Flood inundation images are accessed through BHUVAN's WMS server and images of each month are processed |
| [SENTINEL](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) | NDVI | Monthly | 2024-09 | SENTINEL-2 MSI's images are accessed from Google Earth Engine (GEE) and then processed for each month |
| [IMD](https://imdlib.readthedocs.io/en/latest/) | Rainfall | Monthly | Sep 2024 | Indian Meteorological Department (IMD) data is made available through a python package called [imd-lib](https://imdlib.readthedocs.io/en/latest/). The data is accessed in the form of daily rasters, which are processed for each month |
| [NASADEM](https://www.earthdata.nasa.gov/esds/competitive-programs/measures/nasadem) | Elevation, Slope | One-Time | 2000 | Digital Elevation Model (DEM) is sourced from Google Earth Engine (GEE) in the form of a raster. Slope is calculated from the DEM using a mathematical expression. The rasters are processed to aggregate values for each revenue circle |
| [GCN250](https://gee-community-catalog.org/projects/gcn250/) | Surface runoff | One-Time | 2019 | The Global Curve Numbers (GCN) dataset is available as a raster image on GEE Community Catalog. This raster is processed to calculate aggregate value for each revenue circle |
| [WRIS](https://indiawris.gov.in/wris/) | Distance from rivers, Drainage density | One-Time | 2022 | GIS data accessed from WRIS servers is processed to calculate the variables of interest for each revenue circle |

### Exposure Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing |
|-------------|----------------|-----------|--------------|------------------------|
| [BHARAT MAPS](https://bharatmaps.gov.in/newversion/map.aspx) | Health centers per revenue circle, Road length per revenue circle, Rail length per revenue circle, School per revenue circle | One-Time | 2023-09 | The GIS data from BHARAT MAPS data can be accessed through the ArcGIS REST server. This is a snapshot data that we can access through softwares like QGIS. After accessing the GIS data, we process it to calculate the variables of interest |
| [NERDRR](https://apps.nesdr.gov.in:442/geoserver/web/wicket/bookmarkable/org.geoserver.web.demo.MapPreviewPage?0&filter=false) | Proximity to embankment | One-Time | 2023-09 | The GIS data from NERDRR can be accessed through their Geo Server. After downloading data on embankments, it was processed to calculate the variable of interest |
| [SENTINEL](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR) | NDBI | Monthly | 2023-08 | SENTINEL-2 MSI's images are accessed from Google Earth Engine (GEE) and then processed for each month |

### Vulnerability Variables

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing |
|-------------|----------------|-----------|--------------|------------------------|
| [World Pop](https://www.worldpop.org/) | Population, Sex-Ratio, Aged population (>=65), Children population (<=5) | Yearly | 2024 | Since the national census got delayed we are using World Pop's estimates for every year to calculate population in each revenue circle |
| Mission Antyodaya 2020 | Net sown area, Availability of domestic electricity, Availability of telephone services, Households with piped water connections, Households without sanitary latrines | One-Time | 2020 | Mission Antyodaya 2020 data is processed to find aggregates for each revenue circles. Wherever there are gaps in the Mission Antyodaya data, World Pop estimates are used to cover the gaps |

### Damage and Losses

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing |
|-------------|----------------|-----------|--------------|------------------------|
| [FRIMS](http://www.asdma.gov.in/reports.html) | Population affected, Crop area affected, Roads damaged, Bridges damaged, Embankments damaged, Human lives lost, Animals affected, Animals washed away, Erosion damages, Houses damaged | Monthly | 09-2024 | ASDMA collects Flood damages datasets on a daily basis and makes it available in the form of FRIMS system. We plan to get access to FRIMS datasets through an API access. We would then process it to calculate the variables of interest for each month for each revenue circle |

### Government Response

| Data Source | Data Variables | Frequency | Last Updated | Method of data sourcing |
|-------------|----------------|-----------|--------------|------------------------|
| [FRIMS](http://www.asdma.gov.in/reports.html) | Number of relief camps, Number of relief distribution centres, Number of inmates in relief camps, Relief distributed (Oil, Rice, Dal, Salt) | Monthly | 09-2024 | ASDMA collects Flood relief datasets on a daily basis and makes it available in the form of FRIMS system. We plan to get access to FRIMS datasets through an API access. We would then process it to calculate the variables of interest for each month for each revenue circle |
| [TENDERS](https://assamtenders.gov.in/nicgep/app?page=WebTenderStatusLists&service=page) | Total number of flood related tenders awarded, Total awarded amount of tenders, Tenders - scheme wise (SDRF, SOPD, RIDF), Tenders works wise (Roads, Bridges, Embankments, Erosion), Tenders Type (Immediate measure, Repairs, Preparation, Goods) | Monthly | 09-2024 | Awarded Tenders (AOC) are scraped for each month from the assam tenders website. The scraped data is then processed to calculate flood related tenders. We then geotag each of the flood related tender to a revenue circle to calculate the variables for each revenue circle |
