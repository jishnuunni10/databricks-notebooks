# Databricks notebook source
# Touch Update Account

import requests
import json
from datetime import datetime

# Configuration
API_ENDPOINT = "https://api.example.com/accounts"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"
}

def update_account(account_id, data):
    """
    Update account information
    
    Args:
        account_id: The account ID to update
        data: Dictionary containing update data
    
    Returns:
        Response from API
    """
    url = f"{API_ENDPOINT}/{account_id}"
    
    try:
        response = requests.put(url, headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating account: {e}")
        return None

def touch_account(account_id):
    """
    Touch an account to update its last modified timestamp
    
    Args:
        account_id: The account ID to touch
    """
    data = {
        "last_touched": datetime.now().isoformat(),
        "touch_update": True
    }
    
    result = update_account(account_id, data)
    if result:
        print(f"Successfully touched account {account_id}")
        return result
    else:
        print(f"Failed to touch account {account_id}")
        return None

# Example usage
if __name__ == "__main__":
    # Test account ID
    test_account_id = "12345"
    
    # Touch the account
    result = touch_account(test_account_id)
    
    if result:
        print(f"Account update result: {json.dumps(result, indent=2)}")
