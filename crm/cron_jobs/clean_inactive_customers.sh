#!/bin/bash

# Move to project root
cd "$(dirname "$0")/../.." || exit 1

# Ensure temp directory exists (Windows-safe)
mkdir -p /c/Temp

python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer, Order

one_year_ago = timezone.now() - timedelta(days=365)

inactive_customers = Customer.objects.exclude(
    id__in=Order.objects.filter(
        order_date__gte=one_year_ago
    ).values_list('customer_id', flat=True)
)

count = inactive_customers.count()
inactive_customers.delete()

with open("/c/Temp/customer_cleanup_log.txt", "a") as f:
    f.write(f"{timezone.now().strftime('%Y-%m-%d %H:%M:%S')} - Deleted {count} inactive customers\n")

exit()
EOF
