import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from shop.models import Product, Customer, Order, OrderItem

BATCH = 2000  # adjust for memory

class Command(BaseCommand):
    help = "Generate fake products, customers, and orders"

    def add_arguments(self, parser):
        parser.add_argument('--products', type=int, default=1000)
        parser.add_argument('--orders', type=int, default=100000)
        parser.add_argument('--seed', type=int, default=42)

    def handle(self, *args, **options):
        fake = Faker()
        Faker.seed(options['seed'])
        random.seed(options['seed'])

        products_count = options['products']
        orders_count = options['orders']

        self.stdout.write("Creating products...")
        products = []
        for i in range(products_count):
            products.append(Product(
                sku=f"SKU-{i+1:06d}",
                title=fake.unique.catch_phrase()[:250],
                price=round(random.uniform(5, 500), 2)
            ))
        Product.objects.bulk_create(products, batch_size=BATCH)
        products_qs = list(Product.objects.all())

        self.stdout.write("Creating customers...")
        customers = []
        for i in range(int(max(1000, products_count/1.5))):
            customers.append(Customer(
                email=fake.unique.email(),
                name=fake.name()
            ))
        Customer.objects.bulk_create(customers, batch_size=BATCH)
        customers_qs = list(Customer.objects.all())

        self.stdout.write("Creating orders and order items (this can take a while)...")
        orders_to_create = []
        items_to_create = []
        now = timezone.now()
        start_date = now - timedelta(days=365)  # generate within last year

        for i in range(orders_count):
            # random date in last year
            created_at = start_date + timedelta(seconds=random.randint(0, 365*24*3600))
            customer = random.choice(customers_qs)
            order = Order(customer=customer, created_at=created_at, total=0)
            orders_to_create.append(order)

            if len(orders_to_create) >= BATCH:
                Order.objects.bulk_create(orders_to_create)
                # fetch created orders, to attach items we need their ids
                created_orders = Order.objects.order_by('-id')[:len(orders_to_create)]
                created_orders = list(created_orders)[::-1]  # preserve original order
                for ord_obj in created_orders:
                    num_items = random.randint(1, 5)
                    total = 0
                    for _ in range(num_items):
                        p = random.choice(products_qs)
                        q = random.randint(1, 5)
                        item = OrderItem(order=ord_obj, product=p, quantity=q, unit_price=p.price)
                        items_to_create.append(item)
                        total += q * float(p.price)
                    ord_obj.total = total
                OrderItem.objects.bulk_create(items_to_create, batch_size=BATCH)
                # update totals in bulk (simple per-object save here)
                Order.objects.bulk_update(created_orders, ['total'])
                orders_to_create = []
                items_to_create = []

        # remaining
        if orders_to_create:
            Order.objects.bulk_create(orders_to_create)
            created_orders = Order.objects.order_by('-id')[:len(orders_to_create)]
            created_orders = list(created_orders)[::-1]
            for ord_obj in created_orders:
                num_items = random.randint(1, 5)
                total = 0
                for _ in range(num_items):
                    p = random.choice(products_qs)
                    q = random.randint(1, 5)
                    items_to_create.append(OrderItem(order=ord_obj, product=p, quantity=q, unit_price=p.price))
                    total += q * float(p.price)
                ord_obj.total = total
            OrderItem.objects.bulk_create(items_to_create, batch_size=BATCH)
            Order.objects.bulk_update(created_orders, ['total'])

        self.stdout.write(self.style.SUCCESS("Fake data generation complete."))
