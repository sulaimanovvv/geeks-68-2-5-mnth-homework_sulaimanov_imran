from rest_framework import generics

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductReviewsSerializer,
    CategoryValidateSerializer,
    ProductValidateSerializer,
    ReviewValidateSerializer,
)


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer

        return self.serializer_class


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CategoryValidateSerializer

        return self.serializer_class


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer

        return self.serializer_class


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductValidateSerializer

        return self.serializer_class


class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer

        return self.serializer_class


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ReviewValidateSerializer

        return self.serializer_class


class ProductReviewsListAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductReviewsSerializer
