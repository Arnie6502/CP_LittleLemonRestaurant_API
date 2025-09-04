from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem, Rating
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category', 'category_name', 
                 'description', 'inventory', 'item_of_the_day']

class ManagerListSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','email']

class CartHelpSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['id','title','price']

class CartSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.CharField(source='menuitem.title', read_only=True)
    menuitem_price = serializers.DecimalField(source='menuitem.price', max_digits=6, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'menuitem', 'menuitem_name', 'menuitem_price', 'quantity', 'unit_price', 'price']
        read_only_fields = ['unit_price', 'price']
        
class CartAddSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem','quantity']
        extra_kwargs = {
            'quantity': {'min_value': 1},
        }
class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem']

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.CharField(source='menuitem.title', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'menuitem_name', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    delivery_crew_name = serializers.CharField(source='delivery_crew.username', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_name', 'status', 
                 'total', 'date', 'items', 'items_count']
        read_only_fields = ['user', 'total', 'date']
    
    def get_items_count(self, obj):
        return obj.items.count()

class SingleHelperSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['title','price']
        
class SingleOrderSerializer(serializers.ModelSerializer):
    menuitem = SingleHelperSerializer()
    class Meta():
        model = OrderItem
        fields = ['menuitem','quantity']

class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']