from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializer, MenuItemSerializer, CartSerializer, 
    OrderSerializer, UserSerializer, GroupSerializer, UserRegistrationSerializer
)
from .permissions import IsManagerOrAdmin, IsDeliveryCrewOrManager, IsCustomerOrReadOnly, IsOwnerOrManager


# Custom pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'Little Lemon API',
        'version': '1.0',
        'user': request.user.username if request.user.is_authenticated else 'Anonymous',
        'user_groups': [group.name for group in request.user.groups.all()] if request.user.is_authenticated else [],
        'endpoints': {
            'auth': {
                'register': '/auth/users/',
                'login': '/auth/token/login/',
                'logout': '/auth/token/logout/',
            },
            'api': {
                'categories': '/api/categories/',
                'menu-items': '/api/menu-items/',
                'cart': '/api/cart/',
                'orders': '/api/orders/',
                'groups': '/api/groups/',
            }
        }
    })

# 11, 12: User Registration and Authentication (handled by Djoser)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Customer registration"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 1, 2: Admin and Manager Group Management
class GroupListView(generics.ListAPIView):
    """Admin can view all groups"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]
    
@api_view(['POST'])
@permission_classes([IsAdminUser])
def assign_user_to_manager(request, user_id):
    """1. Admin can assign users to manager group"""
    user = get_object_or_404(User, pk=user_id)
    manager_group, created = Group.objects.get_or_create(name='Manager')
    
    user.groups.add(manager_group)
    
    return Response({
        'message': f'{user.username} assigned to Manager group',
        'user': UserSerializer(user).data
    })

@api_view(['GET'])
@permission_classes([IsManagerOrAdmin])
def manager_group_access(request):
    """2. Access manager group with admin token"""
    manager_group = get_object_or_404(Group, name='Manager')
    managers = User.objects.filter(groups=manager_group)
    
    return Response({
        'group': GroupSerializer(manager_group).data,
        'managers': UserSerializer(managers, many=True).data
    })

# 3, 4: Admin can add menu items and categories
class CategoryListCreateView(generics.ListCreateAPIView):
    """13. Customers can browse all categories / 4. Admin can add categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
    
# Menu Items
class MenuItemListCreateView(generics.ListCreateAPIView):
    """14, 15, 16, 17. Customers can browse, filter, paginate, sort menu items / 3. Admin can add menu items"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'featured']
    ordering_fields = ['price', 'title']
    ordering = ['title']
    search_fields = ['title', 'description']
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        
        # 15. Browse menu items by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        
        # 17. Sort menu items by price
        ordering = self.request.query_params.get('ordering', None)
        if ordering in ['price', '-price']:
            queryset = queryset.order_by(ordering)
        
        return queryset

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsManagerOrAdmin()]
        return [AllowAny()]
    
# Cart
# 18, 19. Cart Management
class CartView(generics.ListCreateAPIView):
    """18, 19. Customers can add menu items to cart and access cart items"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Clear user's cart"""
    Cart.objects.filter(user=request.user).delete()
    return Response({'message': 'Cart cleared successfully'})

# Orders
# 8, 9, 10, 20, 21. Order Management
class OrderListCreateView(generics.ListCreateAPIView):
    """20, 21. Customers can place orders and browse their own orders"""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='Manager').exists():
            # Managers see all orders
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            # 9. Delivery crew can access orders assigned to them
            return Order.objects.filter(delivery_crew=user)
        else:
            # 21. Customers can browse their own orders
            return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """20. Customers can place orders"""
        user = self.request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total
        total = sum(item.price for item in cart_items)
        
        # Create order
        order = serializer.save(user=user, total=total)
        
        # Create order items from cart
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
        
        # Clear cart
        cart_items.delete()

class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrManager]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

# 7. Managers can assign users to delivery crew
@api_view(['POST'])
@permission_classes([IsManagerOrAdmin])
def assign_to_delivery_crew(request, user_id):
    """7. Managers can assign users to the delivery crew"""
    user = get_object_or_404(User, pk=user_id)
    delivery_group, created = Group.objects.get_or_create(name='Delivery crew')
    
    user.groups.add(delivery_group)
    
    return Response({
        'message': f'{user.username} assigned to delivery crew',
        'user': UserSerializer(user).data
    })

# 8. Managers can assign orders to delivery crew
@api_view(['PATCH'])
@permission_classes([IsManagerOrAdmin])
def assign_order_to_delivery_crew(request, order_id):
    """8. Managers can assign orders to the delivery crew"""
    order = get_object_or_404(Order, pk=order_id)
    delivery_crew_id = request.data.get('delivery_crew_id')
    
    if delivery_crew_id:
        delivery_crew = get_object_or_404(User, pk=delivery_crew_id)
        
        # Check if user is in delivery crew group
        if not delivery_crew.groups.filter(name='Delivery crew').exists():
            return Response({'error': 'User is not in delivery crew'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.delivery_crew = delivery_crew
        order.status = 'preparing'
        order.save()
        
        return Response({
            'message': f'Order #{order.id} assigned to {delivery_crew.username}',
            'order': OrderSerializer(order).data
        })
    
    return Response({'error': 'delivery_crew_id is required'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsManagerOrAdmin])
def remove_from_delivery_crew(request, user_id):
    """Remove user from delivery crew"""
    user = get_object_or_404(User, pk=user_id)
    delivery_group = get_object_or_404(Group, name='Delivery crew')
    
    user.groups.remove(delivery_group)
    
    return Response({
        'message': f'{user.username} removed from delivery crew'
    })

# Delivery crew management views
class DeliveryCrewListView(generics.ListAPIView):
    """List all delivery crew members"""
    serializer_class = UserSerializer
    permission_classes = [IsManagerOrAdmin]
    
    def get_queryset(self):
        delivery_group = Group.objects.get(name='Delivery crew')
        return User.objects.filter(groups=delivery_group)

# 10. Delivery crew can update order as delivered
@api_view(['PATCH'])
@permission_classes([IsDeliveryCrewOrManager])
def update_order_status(request, order_id):
    """10. Delivery crew can update an order as delivered"""
    order = get_object_or_404(Order, pk=order_id)
    
    # Check if delivery crew can only update their assigned orders
    if (request.user.groups.filter(name='Delivery crew').exists() and 
        not request.user.groups.filter(name='Manager').exists() and
        order.delivery_crew != request.user):
        return Response({'error': 'You can only update orders assigned to you'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    new_status = request.data.get('status')
    if new_status in ['preparing', 'out_for_delivery', 'delivered']:
        order.status = new_status
        order.save()
        
        return Response({
            'message': f'Order #{order.id} status updated to {new_status}',
            'order': OrderSerializer(order).data
        })
    
    return Response({'error': 'Invalid status. Use: preparing, out_for_delivery, delivered'}, 
                   status=status.HTTP_400_BAD_REQUEST)
