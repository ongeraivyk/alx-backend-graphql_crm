from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport



LOG_FILE = "/tmp/crm_heartbeat_log.txt"
LOG_FILE = "/tmp/lowstockupdates_log.txt"

def logcrmheartbeat():
    message = f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} CRM is alive"
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        client.execute(query)
        message += " | GraphQL endpoint OK"
    except Exception as e:
        message += f" | GraphQL check failed: {str(e)}"

    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")





def update_low_stock():
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    id
                    name
                    stock
                }
                success
            }
        }
        """)

        result = client.execute(mutation)
        updated_products = result['updateLowStockProducts']['updatedProducts']

        with open(LOG_FILE, "a") as f:
            for product in updated_products:
                f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} - "
                        f"Product: {product['name']}, New Stock: {product['stock']}\n")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} - ERROR: {str(e)}\n")



def update_low_stock():
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=False,
            retries=3
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts {
                    id
                    name
                    stock
                }
                success
            }
        }
        """)

        result = client.execute(mutation)
        updated_products = result['updateLowStockProducts']['updatedProducts']

        with open(LOG_FILE, "a") as f:
            for product in updated_products:
                f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} - "
                        f"Product: {product['name']}, New Stock: {product['stock']}\n")

    except Exception as e:
        with open(LOG_FILE, "a") as f:
            f.write(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} - ERROR: {str(e)}\n")
