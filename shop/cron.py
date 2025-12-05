from django.core.cache import cache
from shop.services.analytics import top_selling_products_last_month

CACHE_KEY = "top_selling_last_month_v1"
USERS_CACHE_KEY = "requested_users"

def clear_top_selling_cache():
    cache.delete(CACHE_KEY)
    print("Cleared top-selling cache")

def prewarm_top_selling_cache():
    results = top_selling_products_last_month(limit=10)
    cache.set(CACHE_KEY, results, timeout=None)
    print("Prewarmed top-selling cache")
