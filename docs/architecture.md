# System Architecture

This document provides a detailed explanation of the technical architecture used to cost-optimize and manage billing records using Azure Serverless services.

---

## Overview

The design follows a tiered storage strategy to balance cost-efficiency with high data availability:

- **Hot Data (last 3 months):** Stored in Azure Cosmos DB for fast query and transactional performance.
- **Cold Data (older than 3 months):** Archived to Azure Blob Storage (cool/archive tier) for reduced storage costs.
- **Serverless Logic:** Azure Functions automate data movement (archival) and provide transparent retrieval, ensuring no API contract changes.

---

## Data Flow

### 1. Write Operations
- All new billing records are stored in Azure Cosmos DB via existing API endpoints.

### 2. Archival Process
- A scheduled Azure Function periodically scans Cosmos DB for records older than 3 months.
- These older records are serialized and uploaded to Azure Blob Storage in an archival container.
- After confirming the records are safely stored in Blob Storage, they are deleted from Cosmos DB.
- This guarantees no data is lost during migration.

### 3. Read Operations
- By default, the application/API fetches records from Cosmos DB.
- If a record isn't present (because it was archived), Azure Function retrieves it from Blob Storage and returns it to the API/client.
- This fallback is seamless and invisible to external consumers.

---

## Cost Optimization Rationale

- **Cosmos DB** is reserved for operational, frequently accessed data, drastically reducing premium database storage costs.
- **Azure Blob Storage (cool/archive tier)** is used for long-term, infrequently accessed data, providing substantial cost savings.
- **Azure Functions** handle orchestration without incurring idle compute costs, as they're billed only when used.

---

## Design Considerations

- **Zero Downtime/Data Loss:** Records are only deleted from Cosmos DB after safe archival verification.
- **No API Contract Changes:** The system's read/write interfaces remain unchanged; archival/retrieval logic is encapsulated server-side.
- **Security:** All resources use managed identities and encryption for secure data transfer and storage.
- **Scalability:** The use of serverless architecture ensures the solution automatically adapts to increasing data volumes.

---

## Monitoring & Future Enhancements

- **Diagnostics:** Enable logging and alerting for all Azure Functions, Cosmos DB, and Blob Storage operations for tracking and troubleshooting.
- **Improvements:** Consider implementing lifecycle policies for automatic data expiration, advanced compliance workflows, or additional redundancy as needed.

---

## Architecture Diagram

_Refer to the main architecture diagram in `README.md` for a visual overview._

---

This architecture delivers a robust, low-maintenance, and cost-effective way to manage billing records at scale.

