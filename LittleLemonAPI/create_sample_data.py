from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

from LittleLemonAPI.models import Category, MenuItem

class Command(BaseCommand):
    help = 'Create sample data for Little Lemon API'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))

        # Create groups
        manager_group, created = Group.objects.get_or_create(name='Manager')
        customer_group, created = Group.objects.get_or_create(name='Customer')
        delivery_group, created = Group.objects.get_or_create(name='Delivery crew')

        self.stdout.write('✅ Groups created')

        # Create categories
        appetizers, created = Category.objects.get_or_create(
            slug='appetizers', 
            defaults={'title': 'Appetizers'}
        )
        mains, created = Category.objects.get_or_create(
            slug='mains', 
            defaults={'title': 'Main Courses'}
        )
        desserts, created = Category.objects.get_or_create(
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
                'featured': True
            },
            {
                'title': 'Lemon Chicken',
                'price': 18.99,
                'category': mains,
                'description': 'Grilled chicken with lemon sauce',
                'featured': True
            },
            {
                'title': 'Pasta Primavera',
                'price': 15.99,
                'category': mains,
                'description': 'Fresh pasta with seasonal vegetables',
                'featured': False
            },
            {
                'title': 'Tiramisu',
                'price': 8.99,
                'category': desserts,
                'description': 'Classic Italian dessert',
                'featured': True
            },
            {
                'title': 'Bruschetta',
                'price': 9.99,
                'category': appetizers,
                'description': 'Toasted bread with tomatoes and basil',
                'featured': False
            },
            {
                'title': 'Seafood Risotto',
                'price': 22.99,
                'category': mains,
                'description': 'Creamy risotto with mixed seafood',
                'featured': True
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
                f'📊 Total categories: {Category.objects.count()}\n'
                f'📊 Total groups: {Group.objects.count()}'
            )
        )
