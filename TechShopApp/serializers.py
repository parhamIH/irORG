from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from .models import (
    Product, ProductPackage, Category, BaseCategorys, Brand, BaseColor, 
    Color, Size, Gallery, Comment, Category_Attributes,product_attributes
)


class BaseCategorysSerializer(ModelSerializer):
    class Meta:
        model = BaseCategorys
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class BaseColorSerializer(ModelSerializer):
    class Meta:
        model = BaseColor
        fields = '__all__'


class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PPackageSerializer(ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = ProductPackage
        fields = '__all__'
        read_only_fields = ['final_price']


class GallerySerializer(ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# Detailed/Nested Serializers



class BaseCategorysDetailSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    brands = BrandSerializer(many=True, read_only=True)
    
    class Meta:
        model = BaseCategorys
        fields = '__all__' 


class Category_AttributesSerializer(ModelSerializer):
    class Meta:
        model = Category_Attributes
        fields = '__all__'


class product_attributesSerializer(ModelSerializer):
    class Meta:
        model = product_attributes
        fields = '__all__'



class CategoryNestedSerializer(ModelSerializer):
    subcategories = CategorySerializer(many=True, read_only=True)
    category_attributes = Category_AttributesSerializer(many=True, read_only=True, source='category_attributes')
    class Meta:
        model = Category
        fields = '__all__'
class ProductDetailSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    product_packages = PPackageSerializer(many=True, read_only=True, source='product_packages')
    gallery_images = GallerySerializer(many=True, read_only=True, source='gallery_set')
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    product_attributes = product_attributesSerializer(many=True, read_only=True, source='product_attributes')
    class Meta:
        model = Product
        fields = '__all__'
        
