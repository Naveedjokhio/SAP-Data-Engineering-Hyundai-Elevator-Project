# Hyundai Elevator — SAP Data & Analytics Intelligence Platform

**Enterprise Data Engineering • SAP Datasphere • SAP Analytics Cloud • AWS S3 • IoT Analytics**

Developed by **Naveed Jokhio — Data Engineer**

> Educational engineering case-study implementation inspired by the public Hyundai Elevator / SAP customer story. The project implementation is clearly separated from Hyundai Elevator's documented production solution.

![SAP Analytics Cloud Executive Dashboard](screenshots/sac-executive-dashboard.png)

## Table of Contents

1. [Introduction](#1-introduction)
2. [Business Context](#2-business-context)
3. [Problem Statement](#3-problem-statement)
4. [Hyundai Elevator's Documented SAP Modernization](#4-hyundai-elevators-documented-sap-modernization)
5. [Our Hyundai-Aligned Implementation](#5-our-hyundai-aligned-implementation)
6. [Architecture](#6-architecture)
7. [End-to-End Data Flow](#7-end-to-end-data-flow)
8. [Data Sources and Dataset](#8-data-sources-and-dataset)
9. [SAP Datasphere Data Foundation](#9-sap-datasphere-data-foundation)
10. [Analytical Views and Models](#10-analytical-views-and-models)
11. [Near-Real-Time IoT Pipeline](#11-near-real-time-iot-pipeline)
12. [SAP Analytics Cloud](#12-sap-analytics-cloud)
13. [Smart Insights](#13-smart-insights)
14. [Technology Stack](#14-technology-stack)
15. [Implementation Scope](#15-implementation-scope)
16. [Key Architectural Benefits](#16-key-architectural-benefits)
17. [Limitations and Production Considerations](#17-limitations-and-production-considerations)
18. [Future Improvements](#18-future-improvements)
19. [Key Learnings](#19-key-learnings)
20. [Conclusion](#20-conclusion)
21. [Repository Structure](#21-repository-structure)
22. [References](#22-references)
23. [Disclaimer](#23-disclaimer)

## 1. Introduction

Modern industrial enterprises generate data across ERP, procurement, manufacturing, IoT, maintenance, sales, finance, HR and external systems. The challenge is not only collecting that data; it is integrating it into a trusted analytical foundation that preserves business context and can serve operational and management analytics.

The public Hyundai Elevator SAP customer story describes a complex landscape where data was distributed across regions, flat files, external databases, SAP applications and third-party systems. Hyundai Elevator adopted SAP Datasphere and SAP Analytics Cloud to centralize data and improve access to analytics.

This project uses that case study as its business foundation and builds a Hyundai-aligned implementation combining SAP sample enterprise data, synthetic manufacturing/procurement/maintenance data, historical elevator IoT telemetry, an AWS S3 incremental ingestion path, SAP Datasphere analytical modeling and SAP Analytics Cloud dashboards.

## 2. Business Context

The platform models four operational domains in addition to SAP enterprise data:

- **Procurement:** suppliers, materials, purchase orders and purchase-order items.
- **Manufacturing:** machines, production orders, quality inspections and machine downtime.
- **Elevator IoT:** elevator master data, sensor telemetry and alarms.
- **Maintenance:** technicians, maintenance records and maintenance parts.

SAP sample FI, HR and Sales datasets provide enterprise context such as customers/business partners, products and locations.

## 3. Problem Statement

A fragmented data landscape makes cross-domain analytics difficult. Data can exist in operational systems, local files and departmental applications with different definitions and update cycles. This creates manual reconciliation, duplicated logic and limited visibility.

The target architecture therefore follows a simple principle:

```text
ERP + Sales + HR + Procurement + MES + IoT + Maintenance
                         ↓
                 Central Data Layer
                         ↓
                 Analytical Models
                         ↓
                  Business Analytics
```

## 4. Hyundai Elevator's Documented SAP Modernization

SAP's public customer story states that Hyundai Elevator centralized external data sources, ERP and SRM systems in SAP Datasphere. The platform can also integrate elevator IoT data, manufacturing execution systems and ERP data from overseas subsidiaries. SAP Analytics Cloud is used for visualization, analysis and reporting, while Smart Insights supports AI/ML-assisted discovery.

Conceptually, the documented solution can be represented as:

```text
SAP ERP / SRM + External / Third-Party Sources
              + Elevator IoT + MES
                         ↓
                  SAP Datasphere
                  SAP HANA Cloud
                         ↓
                 Central Data Models
                         ↓
              SAP Analytics Cloud
                         ↓
        Dashboards • Reporting • Insights
```

This section describes the public SAP case. It does **not** imply that Hyundai Elevator uses the AWS/Python ingestion extension implemented in this repository.

## 5. Our Hyundai-Aligned Implementation

The project implements the same centralization principle using the resources available in an educational environment:

```text
SAP Sample Enterprise Data
          +
Synthetic Procurement / Manufacturing / Maintenance
          +
Historical Elevator IoT
          ↓
     SAP Datasphere
          ↓
Associations + SQL Views
          ↓
    Analytic Models
          ↓
SAP Analytics Cloud
          ↓
Dashboards + Smart Insights
```

A separate near-real-time extension adds:

```text
Python IoT Producer → Boto3 → AWS S3 → Datasphere Data Flow
                                      ↓
                                APPEND to IoT Tables
                                      ↓
                              Live Analytical Model
                                      ↓
                              SAC Monitoring
```

## 6. Architecture

### 6.1 Core Analytics Architecture

```text
┌──────────────────────── SOURCE DATA ────────────────────────┐
│ SAP FI / HR / Sales                                        │
│ Procurement • Manufacturing • Elevator IoT • Maintenance   │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
                     SAP Datasphere
                            ↓
                 Tables + Associations
                            ↓
                     SQL Views
                            ↓
                   Analytic Models
                            ↓
                SAP Analytics Cloud
                            ↓
              Dashboards + Smart Insights
```

### 6.2 Incremental IoT Architecture

```text
Python IoT Producer
        ↓
      Boto3
        ↓
      AWS S3
        ↓
Datasphere Connection
        ↓
     Data Flow
        ↓
      APPEND
        ↓
Existing Sensor / Alarm Tables
        ↓
 Views → Analytic Model → SAC
```

## 7. End-to-End Data Flow

Historical SAP and synthetic operational datasets form the initial data foundation. Datasphere relationships connect business entities, SQL views implement analytical logic, and Analytic Models expose controlled measures and dimensions to SAP Analytics Cloud.

For the IoT extension, Python generates new sensor/alarm events and uploads them to AWS S3 using Boto3. Datasphere Data Flows ingest the files using an **append** strategy, preserving historical records while adding new observations. SAC consumes the resulting analytical model for near-real-time monitoring.

## 8. Data Sources and Dataset

The repository contains SAP sample datasets and synthetic operational datasets used by the case study.

### SAP sample domains

- FI
- HR
- Sales

### Synthetic operational domains

- Suppliers
- Materials
- Purchase Orders
- Purchase Order Items
- Machines
- Production Orders
- Quality Inspections
- Machine Downtime
- Elevators
- Elevator Sensor Data
- Elevator Alarms
- Technicians
- Maintenance Records
- Maintenance Parts
- Product Mapping

The synthetic dataset includes approximately **500 elevators**, **1 million historical sensor records**, and **20,000 historical alarm records**. These are project data volumes, not Hyundai Elevator production volumes.

## 9. SAP Datasphere Data Foundation

SAP Datasphere is the central integration and modeling layer. Its project responsibilities include table management, associations, SQL modeling, Data Flows, Task Chains, semantic modeling and downstream SAC consumption.

![SAP Datasphere Data Builder](screenshots/sap-datasphere-data-builder.png)

The live-monitoring implementation includes deployed objects such as:

- `Live Elevator Monitoring` — Analytic Model
- `Live Elevator Sensor Monitor` — Fact View
- `Elevator IoT Analytics` — Fact View
- `Load Live Alarm Data` — Data Flow
- `Load Live Sensor Data` — Data Flow
- `Elevator Live Data Pipeline` — Task Chain
- `Elevator Health Summary` — Fact View
- `Elevator Model Load Analysis` — Fact View
- `Elevator Performance Analytics` — Analytic Model

## 10. Analytical Views and Models

Four primary analytical business views were developed:

- `V_ProcurementPerformance_v2`
- `V_ManufacturingEfficiency`
- `V_ElevatorIoTHealth`
- `V_MaintenanceCostAnalysis`

Four primary domain Analytic Models support SAC consumption:

- `AM_ProcurementPerformance`
- `AM_ManufacturingEfficiency`
- `AM_ElevatorIoTHealth`
- `AM_MaintenanceCostAnalysis`

Additional views/models support live IoT monitoring. A dedicated `Live IoT Readings` count-distinct measure uses `sensor_record_id` to count unique live observations in the live-monitoring model.

## 11. Near-Real-Time IoT Pipeline

The live source view isolates producer-generated records using the `SRLIVE%` identifier convention. The pipeline preserves historical data and appends new records rather than replacing existing tables.

Representative live-monitoring logic:

```sql
SELECT
  sensor_record_id,
  elevator_id,
  event_timestamp,
  elevator_model,
  location_id,
  temperature_c,
  vibration_mm_s,
  motor_current_amp,
  load_percentage,
  operating_status,
  health_status,
  1 AS live_reading_count
FROM V_ELEVATOR_IOT_ANALYTICS
WHERE sensor_record_id LIKE 'SRLIVE%';
```

Because the implemented path is **Python → S3 → Datasphere Data Flow**, it is described as **near-real-time / micro-batch ingestion**, not sub-second true streaming.

## 12. SAP Analytics Cloud

SAP Analytics Cloud is the primary visualization and business-consumption layer. The Executive Dashboard provides fleet-level operational monitoring, including:

- distinct elevators by health status,
- top elevators by load percentage,
- current load monitoring,
- operating status,
- peak live load,
- near-real-time temperature trend,
- near-real-time vibration trend,
- live IoT reading activity.

![Hyundai Elevator Fleet Performance Command Center](screenshots/sac-executive-dashboard.png)

The dashboard demonstrates the separation of responsibilities:

```text
SAP Datasphere = Integration + Modeling + Semantics
SAP Analytics Cloud = Visualization + Exploration + Insights
```

## 13. Smart Insights

SAC Smart Insights provides AI/ML-assisted analytical discovery on top of modeled data. In this project it is used as an analytical capability rather than a custom-trained ML model.

No custom Random Forest, XGBoost, neural network or predictive-maintenance model is claimed in the current implementation.

## 14. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Enterprise Data Platform | SAP Datasphere | Integration, modeling and semantic layer |
| Business Intelligence | SAP Analytics Cloud | Dashboards and analytical exploration |
| External Landing | AWS S3 | Incremental IoT landing layer |
| Programming | Python | IoT event generation and utilities |
| AWS SDK | Boto3 | Uploading generated data to S3 |
| Query / Modeling | SQL | Analytical transformations |
| Ingestion | Datasphere Data Flows | Loading incremental sensor/alarm data |
| Orchestration | Datasphere Task Chains | Pipeline execution |
| AI-Assisted Analytics | SAC Smart Insights | Automated analytical discovery |

## 15. Implementation Scope

- SAP FI / HR / Sales sample data
- 15 synthetic operational datasets
- Procurement, manufacturing, IoT and maintenance domains
- Approximately 1 million historical sensor observations
- Approximately 20,000 historical alarm observations
- Enterprise-to-operational associations
- Four primary analytical SQL views
- Four primary domain Analytic Models
- Dedicated live-IoT views and analytic model
- AWS S3 incremental landing
- Datasphere Data Flows with append semantics
- Datasphere Task Chain
- SAP Analytics Cloud dashboards
- SAC Smart Insights

## 16. Key Architectural Benefits

**Centralized** — multiple enterprise and operational domains are available through one analytical foundation.

**Integrated** — SAP master data provides business context to operational manufacturing, elevator and maintenance datasets.

**Historical + Incremental** — historical records remain available while new IoT events are appended.

**Semantic** — Analytic Models expose business-friendly measures and dimensions instead of raw tables directly to dashboard users.

**Decoupled** — event generation, storage, ingestion, modeling and visualization have separate responsibilities.

**Extensible** — the same foundation can later support stronger streaming, predictive maintenance and production monitoring.

## 17. Limitations and Production Considerations

This repository is a case-study implementation, not Hyundai Elevator's production environment.

- SAP sample content represents enterprise data because a production Hyundai ERP environment is not available.
- Procurement, manufacturing, maintenance and elevator telemetry datasets are synthetic.
- The AWS S3 + Python IoT path is **our implementation**, not a claim about Hyundai Elevator's production IoT transport.
- The implemented IoT path is near-real-time/micro-batch rather than true event-by-event streaming.
- SAC Smart Insights is used, but no custom ML model is implemented.
- Production systems would require stronger security, monitoring, retry handling, data-quality controls, CI/CD and environment separation.

## 18. Future Improvements

Potential extensions include:

- supported event-streaming infrastructure for lower-latency telemetry,
- production ERP integration,
- automated data-quality and freshness checks,
- pipeline observability and alerting,
- CI/CD for Datasphere and supporting code,
- predictive-maintenance experimentation using independently defined failure/maintenance outcomes,
- model registry, monitoring and retraining if ML is introduced.

## 19. Key Learnings

A strong data platform becomes easier to maintain when every layer has a clear responsibility:

```text
Python       → Generate / prepare events
AWS S3       → External landing
Data Flows   → Ingest
Datasphere   → Integrate and model
SQL Views    → Business transformation logic
Analytic Models → Business semantics
SAC          → Analytics and visualization
Smart Insights → AI-assisted analytical discovery
```

The project also demonstrates why historical and live data should be designed to coexist rather than maintaining disconnected analytical pipelines.

## 20. Conclusion

The Hyundai Elevator case study illustrates the value of replacing fragmented analytical processes with a centralized, business-aware data foundation. This project implements those principles using SAP Datasphere and SAP Analytics Cloud, then extends the design with a Python/AWS S3 near-real-time IoT ingestion path.

The resulting architecture connects enterprise, procurement, manufacturing, elevator telemetry and maintenance information through reusable analytical models and dashboards while preserving a clear distinction between the documented Hyundai/SAP case and the educational project extension.

## 21. Repository Structure

```text
hyundai_elevator_complete_package/
├── README.md
├── data/
│   └── sap_sample/
│       ├── FI/
│       ├── HR/
│       └── Sales/
├── hyundai_elevator_synthetic_data/
│   ├── ElevatorSensorData.csv
│   ├── ElevatorAlarms.csv
│   ├── Elevators.csv
│   ├── Manufacturing / Procurement / Maintenance CSVs
│   └── hyundai_elevator_data_dictionary.md
├── src/
│   ├── validate_data.py
│   ├── row_count_check.py
│   ├── pk_check.py
│   └── fk_check.py
├── screenshots/
│   ├── sap-datasphere-data-builder.png
│   └── sac-executive-dashboard.png
├── sql/
├── iot-producer/
├── docs/
├── notebooks/
├── output/
└── logs/
```

## 22. References

- [SAP — Hyundai Elevator: Optimizing the supply chain with a single source of truth](https://www.sap.com/about/customer-stories/hyundai-elevator.html)

## 23. Disclaimer

This repository is an **educational Data Engineering and SAP Data & Analytics case-study implementation inspired by publicly available Hyundai Elevator/SAP material**.

SAP Datasphere modeling, SAP sample datasets, synthetic operational datasets, AWS S3 integration, Python-based IoT generation, Data Flows, Task Chains, Analytic Models and SAC dashboards described as **our implementation** represent this project only and should not be interpreted as Hyundai Elevator's exact current production architecture.

Hyundai Elevator's public SAP case confirms SAP Datasphere, SAP Analytics Cloud, SAP HANA Cloud and integration of SAP/third-party sources including elevator IoT and manufacturing data. It does not publicly establish the AWS S3/Python ingestion design used in this repository.

---

### Author

**Naveed Jokhio**  
**Data Engineer**

Project Focus: **SAP Data Engineering • SAP Datasphere • SAP Analytics Cloud • AWS • IoT Analytics • SQL • Enterprise Data Modeling**
