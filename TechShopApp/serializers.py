from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from .models import (
    BaseCategorys, Category, Brand, BaseColor, Color, Size,
    CategoryAttribute, ProductAttribute, Product, ProductPackage,
    Gallery, Comment
)
from rest_framework import serializers



class CategoryAttributeSerializer(ModelSerializer):
    
    class Meta:
        model = CategoryAttribute
        fields = '__all__'


class ProductAttributeSerializer(ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    attribute_title = serializers.CharField(source='attribute.title', read_only=True)
    
    class Meta:
        model = ProductAttribute
        fields = ['id', 'product', 'attribute', 'attribute_name', 'attribute_title', 'value']


class CategorySerializer(ModelSerializer):
    category_attributes = CategoryAttributeSerializer(many=True, read_only=True, source='category_attributes')
    
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
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    
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


class CategoryNestedSerializer(ModelSerializer):
    subcategories = CategorySerializer(many=True, read_only=True)
    category_attributes = CategoryAttributeSerializer(many=True, read_only=True, source='category_attributes')
    class Meta:
        model = Category
        fields = '__all__'


class ProductDetailSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)
    product_packages = PPackageSerializer(many=True, read_only=True, source='product_packages')
    gallery_images = GallerySerializer(many=True, read_only=True, source='gallery_set')
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    product_attributes = ProductAttributeSerializer(many=True, read_only=True, source='attributes')
    class Meta:
        model = Product
        fields = '__all__'


class BaseCategorysSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    attributes = CategoryAttributeSerializer(many=True, read_only=True)
    class Meta:
        model = BaseCategorys
        fields = '__all__'
