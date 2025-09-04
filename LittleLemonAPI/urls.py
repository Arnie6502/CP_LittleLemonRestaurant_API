from django.urls import path
from . import views

urlpatterns = [
    # API Root
    path('', views.api_root, name='api_root'),
    
    # User Registration (11)
    path('register/', views.register, name='register'),
    
    # Groups Management (1, 2)
    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/manager/access/', views.manager_group_access, name='manager_group_access'),
    path('users/<int:user_id>/assign-manager/', views.assign_user_to_manager, name='assign_manager'),
    
    # Categories (4, 13)
    path('categories/', views.CategoryListCreateView.as_view(), name='categories'),
    
    # Menu Items (3, 14, 15, 16, 17)
    path('menu-items/', views.MenuItemListCreateView.as_view(), name='menu_items'),
    path('menu-items/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu_item_detail'),
    
    # Delivery Crew Management (7)
    path('groups/delivery-crew/users/', views.DeliveryCrewListView.as_view(), name='delivery_crew_list'),
    path('users/<int:user_id>/assign-delivery-crew/', views.assign_to_delivery_crew, name='assign_delivery_crew'),
    path('users/<int:user_id>/remove-delivery-crew/', views.remove_from_delivery_crew, name='remove_delivery_crew'),
    
    # Cart (18, 19)
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # Orders (8, 9, 10, 20, 21)
    path('orders/', views.OrderListCreateView.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/assign-delivery/', views.assign_order_to_delivery_crew, name='assign_order_delivery'),
    path('orders/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
]
