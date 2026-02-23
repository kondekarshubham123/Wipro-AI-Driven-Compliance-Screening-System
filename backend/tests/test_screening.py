import httpx
import asyncio
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_screening():
    async with httpx.AsyncClient() as client:
        # 1. Test Root
        print("\n--- Testing API Root ---")
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}, Body: {response.json()}")

        # 2. Test Safe Order
        print("\n--- Testing Safe Order ---")
        safe_order = {
            "order_id": "ORD-001",
            "customer_id": "CUST-123",
            "items": [
                {"name": "Laptop", "category": "Electronics", "quantity": 1, "price": 1200.0}
            ],
            "shipment": {
                "recipient_name": "John Doe",
                "recipient_address": "123 Main St",
                "recipient_country": "USA"
            }
        }
        response = await client.post(f"{BASE_URL}/screen-order", json=safe_order)
        print(f"Status: {response.status_code}, Result: {response.json()['overall_status']}")

        # 3. Test Sanctioned Entity
        print("\n--- Testing Sanctioned Entity ---")
        sanctioned_order = {
            "order_id": "ORD-002",
            "customer_id": "CUST-456",
            "items": [
                {"name": "Laptop", "category": "Electronics", "quantity": 1, "price": 1200.0}
            ],
            "shipment": {
                "recipient_name": "Alpha Corp (Sanctioned)",
                "recipient_address": "789 Secret St",
                "recipient_country": "Sanctionia"
            }
        }
        response = await client.post(f"{BASE_URL}/screen-order", json=sanctioned_order)
        print(f"Status: {response.status_code}, Result: {response.json()['overall_status']}")
        for check in response.json()['checks']:
            print(f"  - {check['check_name']}: {check['status']} ({check['details']})")

        # 4. Test Restricted Item
        print("\n--- Testing Restricted Item ---")
        restricted_order = {
            "order_id": "ORD-003",
            "customer_id": "CUST-789",
            "items": [
                {"name": "Advanced Drone", "category": "Military Hardware", "quantity": 5, "price": 50000.0}
            ],
            "shipment": {
                "recipient_name": "Tech Corp",
                "recipient_address": "456 Tech Park",
                "recipient_country": "UK"
            }
        }
        response = await client.post(f"{BASE_URL}/screen-order", json=restricted_order)
        print(f"Status: {response.status_code}, Result: {response.json()['overall_status']}")
        for check in response.json()['checks']:
            print(f"  - {check['check_name']}: {check['status']} ({check['details']})")

if __name__ == "__main__":
    # Note: Backend must be running for this test to pass.
    # We will simulate the calls or run if possible.
    try:
        asyncio.run(test_screening())
    except Exception as e:
        print(f"Test execution failed (Is the server running?): {e}")
