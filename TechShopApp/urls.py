from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, BaseCategorysViewSet, CategoryViewSet, BrandViewSet,
    ColorViewSet, BaseColorViewSet, SizeViewSet, CategoryAttributeViewSet,
    ProductAttributeViewSet, ProductPackageViewSet, GalleryViewSet, CommentViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'base-categories', BaseCategorysViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'base-colors', BaseColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'category-attributes', CategoryAttributeViewSet)
router.register(r'product-attributes', ProductAttributeViewSet)
router.register(r'product-packages', ProductPackageViewSet)
router.register(r'gallery', GalleryViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]