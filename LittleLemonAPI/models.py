from unicodedata import category
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.management.base import BaseCommand
from decimal import Decimal


class Command(BaseCommand):
    help = 'Create sample data for Little Lemon API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create groups
        manager_group, created = Group.objects.get_or_create(name='Manager')
        customer_group, created = Group.objects.get_or_create(name='Customer')
        delivery_group, created = Group.objects.get_or_create(name='')

        self.stdout.write('✅ Groups created')

        # Create categories
        appetizers, created = category.objects.get_or_create(
            slug='appetizers', 
            defaults={'title': 'Appetizers'}
        )
        mains, created = category.objects.get_or_create(
            slug='mains', 
            defaults={'title': 'Main Courses'}
        )
        desserts, created = category.objects.get_or_create(
            slug='desserts', 
            defaults={'title': 'Desserts'}
        )

        self.stdout.write('✅ Categories created')

        # Create menu items
        menu_items = [
            {
                'title': 'Greek Salad',
                'price': 12.99,
                'category': appetizers,
                'description': 'Fresh Greek salad with feta cheese',
            },
            {
                'title': 'Lemon Chicken',
                'price': 18.99,
                'category': mains,
                'description': 'Grilled chicken with lemon sauce',
            },
            {
                'title': 'Pasta Primavera',
                'price': 15.99,
                'category': mains,
                'description': 'Fresh pasta with seasonal vegetables',
            },
            {
                'title': 'Tiramisu',
                'price': 8.99,
                'category': desserts,
                'description': 'Classic Italian dessert',
            },
            {
                'title': 'Bruschetta',
                'price': 9.99,
                'category': appetizers,
                'description': 'Toasted bread with tomatoes and basil',
            },
            {
                'title': 'Seafood Risotto',
                'price': 22.99,
                'category': mains,
                'description': 'Creamy risotto with mixed seafood',
            }
        ]

        for item_data in menu_items:
            item, created = MenuItem.objects.get_or_create(
                title=item_data['title'],
                defaults=item_data
            )
            if created:
                self.stdout.write(f'✅ Created: {item.title}')
            else:
                self.stdout.write(f'⚠️  Already exists: {item.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Sample data creation completed!\n'
                f'📊 Total menu items: {MenuItem.objects.count()}\n'
                f'📊 Total categories: {category.objects.count()}\n'
                f'📊 Total groups: {Group.objects.count()}'
            )
        )

class Category(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(db_index=True, default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(max_length=1000, blank=True, default='')
    inventory = models.SmallIntegerField(default=0)
    item_of_the_day = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)], default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('menuitem', 'user')

    def save(self, *args, **kwargs):
        if self.menuitem:
            self.unit_price = self.menuitem.price
            self.price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.menuitem.title}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_crew = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        related_name='delivery_orders', 
        null=True, 
        blank=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(validators=[MinValueValidator(1)], default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.menuitem.title} x {self.quantity}"
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )
    comment = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.menuitem.title} - {self.rating}/5"

    class Meta:
        unique_together = ('user', 'menuitem')

    def stars_display(self):
        """Safe stars display"""
        rating_value = self.rating or 1
        rating_value = max(1, min(5, rating_value))
        return '★' * rating_value + '☆' * (5 - rating_value)