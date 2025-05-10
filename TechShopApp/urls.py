from django.urls import path,include
from .views import ProductListView,ProductDetailView,MainCategoryView




urlpatterns=[
    path('', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('main-category/', MainCategoryView.as_view(), name='main-category'),
]