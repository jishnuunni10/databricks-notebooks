# Databricks notebook source
import requests
import json

# Step 1: Get Access Token
token_url = (
    "https://auth.reltio.com/oauth/token?grant_type=client_credentials"
)
token_headers = {
    "Authorization": "Basic bmlybWFsYWt1bWFyaTU1NTQ2Om0jbXI3cHRWT3FqZ3ljQSRTcjY1JHZlNWdKZXBMY3NS"
}
token_response = requests.post(token_url, headers=token_headers)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")
if not access_token:
    raise Exception("Access token not found in the response.")

# Step 2: Read API call details
api_calls_df = spark.sql(
    "SELECT CUSTOM_API_ID, CUSTOM_API_URL, CUSTOM_API_BODY FROM workspace.mdm_publish.customer_touch_update"
)
api_calls_list = api_calls_df.collect()

# Step 3: Hit APIs and collect results
results = []
for row in api_calls_list:
    api_url = row.CUSTOM_API_URL
    api_body = row.CUSTOM_API_BODY
    customer_id = row.CUSTOM_API_ID
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        payload = json.loads(api_body)
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        status = "success"
        reason = None
    except Exception as e:
        status = "failed"
        reason = str(e)[:250]
    results.append((customer_id, status, reason))

# Step 4: Update customers table
update_df = spark.createDataFrame(
    results, ["customer_id", "status", "reason"]
)
update_df.createOrReplaceTempView("updates")
spark.sql("""
MERGE INTO workspace.mdm_publish.customers AS tgt
USING updates AS src
ON tgt.customer_id = src.customer_id
WHEN MATCHED THEN
  UPDATE SET
    tgt.status = src.status,
    tgt.reason = src.reason
""")