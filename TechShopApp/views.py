from .models import * 
from .serializers import * 
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission, SAFE_METHODS

"""
DRF ModelViewSet Guide:
-----------------------
1. ModelViewSet automatically provides these endpoints:
   - GET /modelname/ - List all objects (list action)
   - POST /modelname/ - Create a new object (create action)
   - GET /modelname/{id}/ - Retrieve an object (retrieve action)
   - PUT /modelname/{id}/ - Update an object (update action)
   - PATCH /modelname/{id}/ - Partially update an object (partial_update action)
   - DELETE /modelname/{id}/ - Delete an object (destroy action)

2. Actions in DRF:
   - Actions map to HTTP methods: list->GET, create->POST, etc.
   - self.action contains the current action name (list, create, retrieve, etc.)
   - Custom actions can be added with the @action decorator

3. Routing:
   - ViewSets are connected to URLs via a Router (see urls.py)
   - Router automatically creates URL patterns for all standard actions
   - For custom actions, the URL is: /modelname/{id}/action_name/ for detail=True 
     or /modelname/action_name/ for detail=False
"""

class IsAdminOrReadOnly(BasePermission):
    """
    کلاس سفارشی مجوز دسترسی:
    - به همه کاربران اجازه دسترسی خواندن می‌دهد (GET, HEAD, OPTIONS)
    - فقط به ادمین‌ها اجازه اعمال تغییرات (POST, PUT, PATCH, DELETE) می‌دهد
    
    SAFE_METHODS شامل: GET, HEAD, OPTIONS
    """
    
    def has_permission(self, request, view):
        # اگر متد درخواست یک متد امن باشد (فقط مشاهده)، دسترسی به همه کاربران
        if request.method in SAFE_METHODS:
            return True
        
        # در غیر این صورت، فقط ادمین‌ها مجوز دارند
        return request.user and request.user.is_staff

class ProductViewSet(ModelViewSet):
    """
    ViewSet for Product model - handles all CRUD operations.
    
    Endpoints:
    - GET /products/ - List all products
    - POST /products/ - Create a new product
    - GET /products/{id}/ - Get product details (uses ProductDetailSerializer)
    - PUT/PATCH /products/{id}/ - Update a product
    - DELETE /products/{id}/ - Delete a product
    - GET /products/{id}/gallery/ - Get product gallery images (custom action)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        """
        روش دیگر برای تنظیم مجوزهای دسترسی با بررسی اکشن:
        - اگر اکشن create, update, partial_update یا destroy باشد: فقط ادمین‌ها دسترسی دارند
        - برای اکشن‌های دیگر (list, retrieve): همه کاربران دسترسی دارند
        
        این روش نسبت به استفاده از IsAdminOrReadOnly انعطاف‌پذیری بیشتری دارد
        و می‌توان برای هر اکشن به صورت جداگانه تصمیم گرفت.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def get_serializer_class(self):
        """
        Use different serializers based on the action.
        
        For 'retrieve' action (GET detail), use ProductDetailSerializer which includes more data.
        For all other actions, use the standard ProductSerializer.
        
        'self.action' is automatically set by DRF based on the HTTP method and URL pattern.
        """
        if self.action == 'retrieve':  # in ModelViewSet action after routing finde method 
            return ProductDetailSerializer
        return ProductSerializer
    
    @action(detail=True, methods=['get'])
    def gallery(self, request, pk=None):
        """
        Custom action to get all gallery images for a specific product.
        
        URL: /products/{id}/gallery/
        HTTP Method: GET
        
        @action decorator parameters:
        - detail=True: This action is for a specific object (requires an ID)
        - methods=['get']: This action only responds to GET requests
        """
        product = self.get_object()  # Gets the product based on the URL's pk parameter
        gallery = Gallery.objects.filter(product=product)
        serializer = GallerySerializer(gallery, many=True)
        return Response(serializer.data)

class BaseCategorysViewSet(ModelViewSet):
    """
    ViewSet for BaseCategorys model.
    
    Uses different serializers for list and detail views:
    - List view: BaseCategorysSerializer
    - Detail view: BaseCategorysDetailSerializer (includes related categories and brands)
    """
    queryset = BaseCategorys.objects.all()
    serializer_class = BaseCategorysSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند
    
    def get_serializer_class(self):
        """
        Select appropriate serializer based on the current action.
        Detail view needs more information, so use the detailed serializer.
        """
        if self.action == 'retrieve':
            return BaseCategorysDetailSerializer
        return BaseCategorysSerializer

class CategoryViewSet(ModelViewSet):
    """
    ViewSet for Category model.
    
    Custom actions:
    - GET /categories/{id}/products/ - Get all products in a specific category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند
    
    def get_serializer_class(self):
        """
        Use CategoryNestedSerializer for detail view to include subcategories.
        """
        if self.action == 'retrieve':
            return CategoryNestedSerializer
        return CategorySerializer
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Get all products that belong to this category.
        
        URL: /categories/{id}/products/
        HTTP Method: GET
        """
        category = self.get_object()
        products = Product.objects.filter(categories=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class BrandViewSet(ModelViewSet):
    """
    ViewSet for Brand model.
    
    Custom actions:
    - GET /brands/{id}/products/ - Get all products for a specific brand
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """
        Get all products for this brand.
        
        URL: /brands/{id}/products/
        HTTP Method: GET
        """
        brand = self.get_object()
        products = Product.objects.filter(brand=brand)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ColorViewSet(ModelViewSet):
    """
    ViewSet for Color model. Provides standard CRUD operations.
    
    Endpoints:
    - GET /colors/ - List all colors
    - POST /colors/ - Create a new color
    - GET /colors/{id}/ - Get color details
    - PUT/PATCH /colors/{id}/ - Update a color
    - DELETE /colors/{id}/ - Delete a color
    """
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند

class BaseColorViewSet(ModelViewSet):
    """
    ViewSet for BaseColor model. Provides standard CRUD operations.
    """
    queryset = BaseColor.objects.all()
    serializer_class = BaseColorSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند

class SizeViewSet(ModelViewSet):
    """
    ViewSet for Size model. Provides standard CRUD operations.
    """
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند

class CategoryAttributeViewSet(ModelViewSet):
    """
    ViewSet for CategoryAttribute model. Provides standard CRUD operations.
    """
    queryset = CategoryAttribute.objects.all()
    serializer_class = CategoryAttributeSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند

class ProductAttributeViewSet(ModelViewSet):
    """
    ViewSet for ProductAttribute model. Provides standard CRUD operations.
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند

class ProductPackageViewSet(ModelViewSet):
    """
    ViewSet for ProductPackage model.
    
    Supports filtering by product_id query parameter:
    GET /product-packages/?product_id=123
    """
    queryset = ProductPackage.objects.all()
    serializer_class = PPackageSerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند
    
    def get_queryset(self):
        """
        Override get_queryset to support filtering by product_id query parameter.
        
        Example:
        GET /product-packages/?product_id=123
        """
        queryset = ProductPackage.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class GalleryViewSet(ModelViewSet):
    """
    ViewSet for Gallery model.
    
    Supports filtering by product_id query parameter:
    GET /gallery/?product_id=123
    """
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [IsAdminOrReadOnly]  # اعمال مجوز دسترسی - فقط ادمین می‌تواند ایجاد، ویرایش و حذف کند
    
    def get_queryset(self):
        """
        Override get_queryset to support filtering by product_id query parameter.
        
        Example:
        GET /gallery/?product_id=123
        """
        queryset = Gallery.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class CommentViewSet(ModelViewSet):
    """
    ViewSet for Comment model.
    
    Features:
    - Requires authentication (permission_classes = [IsAuthenticated])
    - Automatically sets the user when creating a comment
    - Supports filtering by product_id query parameter
    - Custom action 'my_comments' to list the current user's comments
    
    Endpoints:
    - GET /comments/?product_id=123 - Get comments (optionally filtered by product)
    - POST /comments/ - Add a new comment (user is set automatically)
    - GET /comments/my_comments/ - Get all comments by the current user
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # User must be logged in to interact with comments
    
    def get_queryset(self):
        """
        Override get_queryset to support filtering by product_id query parameter.
        """
        queryset = Comment.objects.all()
        product_id = self.request.query_params.get('product_id', None)
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
    def perform_create(self, serializer):
        """
        Override perform_create to automatically set the user to the current user.
        This ensures comments are always associated with the logged-in user.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_comments(self, request):
        """
        Custom action to get all comments made by the current user.
        
        URL: /comments/my_comments/
        HTTP Method: GET
        """
        comments = Comment.objects.filter(user=request.user)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """
        Override get_permissions to customize permissions for different actions.
        - Create, list, retrieve: Authenticated users can view and create comments
        - Update, destroy: Only admins can modify or delete comments
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
