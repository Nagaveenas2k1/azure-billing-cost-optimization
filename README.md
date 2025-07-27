# Azure Cost Optimization: Billing Records Management

## Overview

Efficient storage solution for billing records in Azure—minimizing costs using Cosmos DB (hot store) and Blob Storage (cold store/archive), with transparent retrieval and no API changes.

## Architecture

### Architecture

![Architecture Diagram](architecture.png)

- **Hot Store:** Azure Cosmos DB (last 3 months of records)
- **Cold Store:** Azure Blob Storage, cool/archive tier (records >3 months old)
- **Bridge:** Azure Functions for archival and proxy retrieval

## Key Features

- Cost-efficient: hot/cold data split
- No API changes required
- Automated, serverless archival pipeline
- Seamless user experience (no data loss/downtime)

## Getting Started

### Prerequisites:

- Python 3.8+
- Azure CLI
- Azure Functions Core Tools

### Install dependencies:

pip install -r requirements.txt


### Deploy Resources:

bash scripts/deploy_resources.sh


### Configure and Deploy Functions:

- Fill in Cosmos DB and Blob Storage connection info in Python scripts.
- Deploy or run locally using Azure Functions Core Tools.

## Code Structure:

- `/archive/`: Archival function source
- `/retrieval/`: Retrieval function source
- `/scripts/`: Shell scripts for Azure resource deployment
- `/docs/`: Detailed design/decisions

## Note:

Refer to `docs/architecture.md` for deeper discussion on design, cost models, and operational notes.

---

## Requirements Met

| Requirement           | Solution Approach                                        |
|-----------------------|----------------------------------------------------------|
| Simplicity            | Serverless functions, no major infrastructure changes    |
| No Data Loss/Downtime | Confirm write-before-delete, staggered migration         |
| No API Changes        | Proxy, preserves contract and behavior                   |
| Cost Optimization     | Cold data in lowest cost storage, hot in Cosmos DB       |

---

## Author

S Nagaveena
