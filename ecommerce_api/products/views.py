from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

CACHE_TIMEOUT = 3600  # 1 hour

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        cached = cache.get('categories')
        if cached:
            return Response(cached)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set('categories', serializer.data, CACHE_TIMEOUT)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete('categories')

    def perform_update(self, serializer):
        serializer.save()
        cache.delete('categories')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete('categories')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        cached = cache.get('products_filtered_' + str(request.query_params))
        if cached:
            return Response(cached)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data).data

        cache.set('products_filtered_' + str(request.query_params), data, CACHE_TIMEOUT)
        return Response(data)

    def perform_create(self, serializer):
        serializer.save()
        cache.delete_pattern("products*")

    def perform_update(self, serializer):
        serializer.save()
        cache.delete_pattern("products*")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete_pattern("products*")