# Top Selling Products API

This Django project provides a fast, cached API endpoint to fetch the top-selling products of the last month using Redis for caching and django-crontab for automated cache clearing and prewarming.

## Features

- Efficient models: Product, Order, OrderItem, Customer
- Bulk data generation for testing
- Optimized query to get top 10 best-selling products
- Redis caching for fast API responses
- Automated cache clearing at 2 AM via django-crontab
- Optional prewarming to populate cache immediately after clearing

## Requirements

- Python 3.10+
- Django 4.x
- Django REST Framework
- Redis
- django-redis
- django-crontab
- Faker (for fake data generation)

Install dependencies:
```
pip install django djangorestframework django-redis django-crontab Faker
```

## Setup

1. Clone project:
```
git clone <repo_url>
cd <project_folder>
```

2. Migrate database:
```
python manage.py makemigrations
python manage.py migrate
```


3. Define cron jobs in settings.py:
```
CRONJOBS = [
    ('0 2 * * *', 'core.cron.clear_redis_cache'),
    ('10 2 * * *', 'core.cron.prewarm_redis_cache'),
]
```



4. Add cron jobs to system:
```
python manage.py crontab add
python manage.py crontab show
```

5. Generate fake data (optional):
```
python manage.py generate_fake_data --products 1000 --orders 100000
```

## API Endpoint

GET /api/top-selling-products/

Response:
```
{
  "cached": true,
  "results": [
    {"title": "Product A", "total_sales": 150},
    {"title": "Product B", "total_sales": 120},
    ...
  ]
}
```