# Databricks notebook source
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("ReltioAPICaller") \
    .getOrCreate()

# --- Step 1: Get Access Token ---
token_url = "https://auth.reltio.com/oauth/token?grant_type=client_credentials"
token_headers = {
    'Authorization': 'Basic bmlybWFsYWt1bWFyaTU1NTQ2Om0jbXI3cHRWT3FqZ3ljQSRTcjY1JHZlNWdKZXBMY3NS'
}

try:
    token_response = requests.post(token_url, headers=token_headers)
    token_response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
    access_token = token_response.json().get("access_token")
    if not access_token:
        raise Exception("Access token not found in the response.")
    print("Access Token obtained successfully.")
except requests.exceptions.RequestException as e:
    raise Exception(f"Failed to get access token: {e}")

# --- Step 2: Read API call details from the view ---
try:
    api_calls_df = spark.sql("SELECT CUSTOM_API_URL, CUSTOM_API_BODY FROM mdm_publish.customer_touch_update")
    print(f"Successfully loaded {api_calls_df.count()} API calls from the view.")
except Exception as e:
    raise Exception(f"Failed to read from view mdm_publish.customer_touch_update: {e}")

# --- Step 3: Define a function to hit the API ---
def hit_reltio_api(api_url, api_body, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    try:
        # Assuming api_body is a string representation of a JSON object
        # It needs to be sent as a dictionary/JSON object for requests.post(json=...)
        # or as a string for requests.post(data=...) with Content-Type application/json
        # Given your image, api_body is "[{"value": "true"}]" which is a JSON array string.
        # It's safer to load it as a JSON object before sending.
        import json
        payload = json.loads(api_body)
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"Successfully posted to {api_url}. Response: {response.status_code}")
        return True, response.status_code, response.text
    except requests.exceptions.RequestException as e:
        print(f"Error posting to {api_url}: {e}")
        return False, None, str(e)
    except json.JSONDecodeError as e:
        print(f"Error decoding API body for {api_url}: {e}")
        return False, None, str(e)


# --- Step 4: Iterate and hit APIs (using foreach for side effects) ---
# It's important to understand that `foreach` and `map` operations in PySpark
# distribute the work across the cluster. If `hit_reltio_api` relies on
# objects (like `access_token`) that are not broadcasted or are not
# available on worker nodes, it can cause issues.
# For simplicity, we'll collect the data and iterate locally, or use a UDF
# with careful handling of the access token.

# Option 1: Collect data to driver and process (suitable for smaller datasets)
# This is simpler to implement if the number of API calls is not extremely large,
# as it avoids serialization issues of the 'requests' library with UDFs directly.

api_calls_list = api_calls_df.collect()

results = []
for row in api_calls_list:
    api_url = row.CUSTOM_API_URL
    api_body = row.CUSTOM_API_BODY
    success, status_code, response_text = hit_reltio_api(api_url, api_body, access_token)
    results.append({
        "url": api_url,
        "success": success,
        "status_code": status_code,
        "response_text": response_text
    })

# Print results
print("\n--- API Call Results ---")
for res in results:
    print(f"URL: {res['url']}, Success: {res['success']}, Status Code: {res['status_code']}, Response: {res['response_text'][:100]}...") # Truncate response for readability

# Option 2: Using Pandas UDF (more scalable for larger datasets, requires careful setup)
# This option is more complex as it requires distributing the access token and
# handling external libraries within the UDF. For simplicity and given the
# context, Option 1 is often preferred for batch API calls unless the dataset
# is massive and parallel processing is absolutely critical.
# For Option 2, you would need to broadcast the access token and potentially
# handle library dependencies on worker nodes.

spark.stop()