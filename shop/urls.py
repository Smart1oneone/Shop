from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', products_view, name='products'),
    path('<slug:slug>/', product_details_view, name='product_details'),
    path('search/<slug:slug>', category_list, name='category_list'),


]