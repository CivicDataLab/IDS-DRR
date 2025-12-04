# Architecture Overview

This section describes the overall system architecture for the IDS-DRR platform.

## Data Flow

The overall data flow between various steps is summarized below:

1. **Identify**: Determine required data, sources, and variables
2. **Collect**: Gather raw data via APIs, QGIS, or scraping; start the data pipeline by storing it
3. **Process**: Clean, transform, and standardize data, saving relevant variables in a database
4. **Model**: Perform data modeling and store the outputs
5. **Analyze**: Build a data analytics layer with access APIs
6. **Front-End**: Develop a front-end analytics page
7. **Publish**: Create a data publishing platform (opub) for historical and real-time data with admin-only upload access
8. **List**: Implement a frontend page for accessing published datasets

![data flow](https://github.com/CivicDataLab/IDS-DRR/assets/39596102/2b0d1356-e6d8-4676-a9ba-0f31eaca18c5)

## Platform Components

The system is broadly divided into 2 sections:

### User Pane

The user-facing components of the platform that allow decision-makers to:

- View interactive maps with flood risk indicators
- Filter data by time period, district, and revenue circle
- Generate tailored reports
- Access historical and real-time data

### Data Pane

The backend components that handle:

- Data ingestion from multiple sources
- Data processing and transformation
- Risk model calculations
- API endpoints for data access
- Data storage and management

## Technical Stack

- **Data Pipeline & Orchestration**: RabbitMQ, Prefect
- **Data Processing**: Python, QGIS
- **Statistical Modeling**: Gurobi (for DEA), TOPSIS implementation
- **Data Sources**: Google Earth Engine, various government APIs and portals
- **Frontend**: Interactive maps and dashboards
