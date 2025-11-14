from django.db.models import Sum, F
from django.utils import timezone
from datetime import datetime, timedelta

from shop.models import Product


def get_last_month_period():
    now = timezone.now()
    first_of_this_month = datetime(year=now.year, month=now.month, day=1, tzinfo=now.tzinfo)
    last_month_end = first_of_this_month - timedelta(seconds=1)
    last_month_start = datetime(year=last_month_end.year, month=last_month_end.month, day=1, tzinfo=now.tzinfo)
    return last_month_start, last_month_end

def top_selling_products_last_month(limit=10):
    start, end = get_last_month_period()
    qs = (Product.objects
          .filter(order_items__order__created_at__gte=start, order_items__order__created_at__lte=end)
          .annotate(total_sales=Sum('order_items__quantity'))
          .order_by('-total_sales')
          .values('id', 'title', 'total_sales')[:limit])
    return list(qs)
