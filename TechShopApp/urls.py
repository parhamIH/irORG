from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, BaseCategorysViewSet, CategoryViewSet, BrandViewSet,
    ColorViewSet, BaseColorViewSet, SizeViewSet, CategoryAttributeViewSet,
    ProductAttributeViewSet, ProductPackageViewSet, GalleryViewSet, CommentViewSet
)

"""
DRF Router Explanation:
-----------------------
The DefaultRouter class automatically creates URL patterns for our ViewSets.

For each ViewSet registered with router.register():
- The first argument ('products', 'categories', etc.) defines the URL prefix
- The second argument is the ViewSet class that will handle the requests

For each registered ViewSet, the router creates these URL patterns:
- LIST:   /prefix/ [name='prefix-list'] - GET to list all, POST to create
- DETAIL: /prefix/{pk}/ [name='prefix-detail'] - GET one, PUT/PATCH/DELETE

For ViewSets with @action decorator:
- Detail actions: /prefix/{pk}/action_name/
- List actions: /prefix/action_name/

Example URLs with our router:
- GET /products/ - List all products
- POST /products/ - Create a new product
- GET /products/5/ - Get details for product with id=5
- GET /products/5/gallery/ - Get gallery for product with id=5 (custom action)
- GET /comments/my_comments/ - Get all comments by current user (list action)
"""

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
    # Include all the router-generated URLs in our urlpatterns
    # This single line creates all the necessary URL patterns for our ViewSets
    path('', include(router.urls)),
]