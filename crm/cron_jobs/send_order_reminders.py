#!/usr/bin/env python

import os
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Log file (Windows-safe)
LOG_FILE = "/c/Temp/order_reminders_log.txt"

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url=GRAPHQL_URL,
    verify=False,
    retries=3,
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")

# GraphQL query to get orders from last 7 days
query = gql(
    """
    query($since: DateTime!) {
      orders(orderDate_Gte: $since) {
        id
        customer {
          email
        }
      }
    }
    """
)

try:
    result = client.execute(query, variable_values={"since": seven_days_ago})

    orders = result.get("orders", [])

    with open(LOG_FILE, "a") as f:
        for order in orders:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
                    f"Order ID: {order['id']}, Customer: {order['customer']['email']}\n")

    print("Order reminders processed!")

except Exception as e:
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}\n")
    print("Error executing order reminders script:", e)
