from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from shop.services.analytics import top_selling_products_last_month

CACHE_KEY = "top_selling_last_month_v1"
USERS_CACHE_KEY = "requested_users"


class TopSellingProductsAPIView(APIView):
    """
    GET /api/top-selling-products/
    Returns top 10 products for last month: [{title, total_sales}, ...]
    """
    def get(self, request):
        data = cache.get(CACHE_KEY)
        cache.client.get_client().sadd(USERS_CACHE_KEY, request.user.username)
        if data is not None:
            return Response({"cached": True, "results": data})

        # Cache miss: compute and cache (fast DB aggregation)
        results = top_selling_products_last_month(limit=10)

        # Normalize total_sales to int (or float)
        for r in results:
            r['total_sales'] = int(r.get('total_sales') or 0)

        cache.set(CACHE_KEY, results, timeout=None)  # we'll manage invalidation externally
        return Response({"cached": False, "results": results})
