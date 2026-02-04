# Databricks Notebooks - Reltio API Integration

This repository contains Databricks notebooks for integrating with Reltio API to perform customer touch updates.

## 📋 Overview

**Workspace**: `https://dbc-954e6b63-50c7.cloud.databricks.com`  
**User**: `chakkappazhamseries1@gmail.com`  
**Path**: `/Workspace/Users/chakkappazhamseries1@gmail.com`

## 📁 Notebooks

### 1. Touch_update_account.py

Basic Reltio API caller with console logging.

**Features:**
- OAuth token authentication with Reltio
- Reads API URLs and bodies from Spark SQL view
- Posts requests to Reltio API endpoints
- Collects and prints results to console
- Processes on driver node (suitable for smaller datasets)

**Data Source:**
```sql
SELECT CUSTOM_API_URL, CUSTOM_API_BODY 
FROM mdm_publish.customer_touch_update
```

**Output:** Console logs only

---

### 2. TUbot_upd.py

Enhanced version with database update capability.

**Features:**
- OAuth token authentication with Reltio
- Reads from `workspace.mdm_publish.customer_touch_update` (includes CUSTOM_API_ID)
- Posts requests to Reltio API endpoints
- Tracks success/failure status for each API call
- Updates customer records in database with status and reason
- Uses MERGE statement for database updates

**Data Source:**
```sql
SELECT CUSTOM_API_ID, CUSTOM_API_URL, CUSTOM_API_BODY 
FROM workspace.mdm_publish.customer_touch_update
```

**Output:** Updates `workspace.mdm_publish.customers` table

**Database Update:**
```sql
MERGE INTO workspace.mdm_publish.customers AS tgt
USING updates AS src
ON tgt.customer_id = src.customer_id
WHEN MATCHED THEN
  UPDATE SET
    tgt.status = src.status,
    tgt.reason = src.reason
```

---

## 🔑 Key Differences

| Feature | Touch_update_account.py | TUbot_upd.py |
|---------|------------------------|---------------|
| **Fields Read** | CUSTOM_API_URL, CUSTOM_API_BODY | CUSTOM_API_ID, CUSTOM_API_URL, CUSTOM_API_BODY |
| **Data Source** | `mdm_publish.customer_touch_update` | `workspace.mdm_publish.customer_touch_update` |
| **Output** | Console logs only | Database table updates |
| **Error Handling** | Detailed logging | Status tracking in database |
| **Database Updates** | None | MERGE into customers table |
| **Best For** | Testing/debugging | Production use |

---

## 🚀 Usage

### Prerequisites
- Databricks workspace access
- Reltio API credentials (configured in notebooks)
- Access to `mdm_publish` schema and tables

### Running the Notebooks

1. Import notebooks to your Databricks workspace
2. Ensure required tables/views exist:
   - `mdm_publish.customer_touch_update` or `workspace.mdm_publish.customer_touch_update`
   - `workspace.mdm_publish.customers` (for TUbot_upd.py)
3. Attach to a running cluster
4. Run all cells

---

## 🔒 Security Note

⚠️ **Important**: These notebooks contain embedded OAuth credentials. For production use:
- Store credentials in Databricks Secrets
- Use Secret Scopes to access sensitive information
- Never commit credentials to version control

---

## 📊 Architecture

```
┌─────────────────────┐
│  Databricks         │
│  Notebook           │
└──────┬──────────────┘
       │
       ├─► OAuth Token Request
       │   (Reltio Auth API)
       │
       ├─► Read from View
       │   (customer_touch_update)
       │
       ├─► POST Requests
       │   (Reltio API)
       │
       └─► Update Database
           (customers table)
```

---

## 📝 License

This project is for internal use.

---

## 👤 Author

Maintained by the Data Engineering team.