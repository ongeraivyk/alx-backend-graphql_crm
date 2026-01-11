from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_heartbeat_log.txt"

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
