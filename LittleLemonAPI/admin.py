from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'featured', 'item_of_the_day', 'inventory']
    list_filter = ['category', 'featured', 'item_of_the_day']
    search_fields = ['title', 'description']
    list_editable = ['price', 'featured', 'item_of_the_day', 'inventory']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
    list_filter = ['user']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
    list_filter = ['status', 'date', 'delivery_crew']
    search_fields = ['user__username']
    list_editable = ['status', 'delivery_crew']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menuitem', 'quantity', 'unit_price', 'price']
    list_filter = ['order__status']
    
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'menuitem', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
