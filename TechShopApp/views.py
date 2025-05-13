from .models import * 
from .serializers import * 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['get'])
    def gallery(self, request, pk=None):
        product = self.get_object()
        gallery = Gallery.objects.filter(product=product)
        serializer = GallerySerializer(gallery, many=True)
        return Response(serializer.data)

class BaseCategorysViewSet(ModelViewSet):
    queryset = BaseCategorys.objects.all()
    serializer_class = BaseCategorysSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BaseCategorysDetailSerializer
        return BaseCategorysSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryNestedSerializer
        return CategorySerializer
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = Product.objects.filter(categories=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        brand = self.get_object()
        products = Product.objects.filter(brand=brand)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ColorViewSet(ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class BaseColorViewSet(ModelViewSet):
    queryset = BaseColor.objects.all()
    serializer_class = BaseColorSerializer

class SizeViewSet(ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer

class CategoryAttributeViewSet(ModelViewSet):
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer

class ProductAttributeViewSet(ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

class ProductPackageViewSet(ModelViewSet):
    queryset = ProductPackage.objects.all()
    serializer_class = PPackageSerializer
    
    def get_queryset(self):
        queryset = ProductPackage.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class GalleryViewSet(ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    
    def get_queryset(self):
        queryset = Gallery.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_comments(self, request):
        comments = Comment.objects.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
