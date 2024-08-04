from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('search_products/', search_products, name='search-products'),
    path('<slug:slug>/', product_details_view, name='product-detail'),
    path('search/<slug:slug>', category_list, name='category-list'),


]