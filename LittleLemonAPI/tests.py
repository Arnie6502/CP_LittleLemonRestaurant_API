from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category-list'),
    path('menu-items/', views.MenuItemsView.as_view(), name='menu-items-list'),
]