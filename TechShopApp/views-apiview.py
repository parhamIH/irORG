from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from .models import *
from .serializers import *


# Create your views here.


class ProductListView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get' , 'post']  

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    
    def post(self ,request):
        serializer = ProductSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    
    def put(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class MainCategoryView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['get',"post"]

    def get(self, request):
        main_categories = BaseCategorys.objects.all()
        serializer = BaseCategorysSerializer(main_categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BaseCategorysSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
