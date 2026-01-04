# Uber Data Analytics Engineering Pipeline

## Project Overview
I built an end-to-end data engineering pipeline to process and analyze Uber trip records. The goal was to transform raw data into a structured format (Star Schema) suitable for analytics, orchestrate the workflow using Mage.ai, and build dashboards for business insights.

## Architecture Diagram
![Architecture Diagram]()
*( Architecture Diagram)*

## Technologies
- **Language**: Python
- **Transformation**: Pandas (Data cleaning, Dimensional Modeling)
- **Orchestration**: Mage.ai (ETL Pipeline management)
- **Storage**: Local Storage / Google Cloud Storage (Architecture designed for Cloud)
- **Visualization**: Google Looker Studio & Power BI

## Data Model
I designed a **Star Schema** to optimize the data for analytical queries.

### Schema Structure
- **Fact Table**: `fact_table`
  - Contains keys, revenue metrics, and trip metrics.
  - **Design Decision**: I deliberately avoided creating unnecessary dimensions for single values (like Passenger Count or Trip Distance), keeping them as measures in the Fact Table to improve query performance.

- **Dimension Tables**:
  - `dim_datetime`
  - `dim_payment_type`
  - `dim_rate_code`
  - `dim_vendor`

### Transformation Logic
- **Data Conversion**: Converted timestamps to datetime objects.
- **Deduplication**: Removed duplicates and assigned unique `trip_id` keys.
- **Data Quality Checks**: Filtered out bad data (e.g., trips with 0 passengers, 0 distance, or negative fares) to ensure analytics accuracy.
- **Orchestration**: Used Mage.ai to break the process into modular blocks (Loader -> Transformer -> Exporter).

## Step-by-Step Execution

### 1. Install Mage
```bash
pip install mage-ai
```

### 2. Initialize Project
```bash
mage start project_name
```

### 3. Run the Pipeline
Execute the ETL pipeline within the Mage UI.

## Dashboard Results
The final results are visualized in Google Looker Studio and Power BI, providing insights such as:
- **Revenue by Payment Type**
- **Map Visualization** of trip routes and densities


