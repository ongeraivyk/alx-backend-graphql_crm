from celery import shared_task
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/crm_report_log.txt"

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        customersCount
        ordersCount
        totalRevenue
    }
    """)

    result = client.execute(query)

    log_entry = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Report: {result['customersCount']} customers, "
        f"{result['ordersCount']} orders, "
        f"{result['totalRevenue']} revenue\n"
    )

    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
