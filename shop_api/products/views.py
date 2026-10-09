from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        data = CategorySerializer(categories, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        validate_serializer = CategoryValidateSerializer(data=request.data)

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        name = validate_serializer.validated_data.get('name')

        category = Category.objects.create(
            name=name
        )

        data = CategorySerializer(category, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(
            data='Category not found!',
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = CategorySerializer(category, many=False).data

        return Response(data=data)

    elif request.method == 'PUT':
        validate_serializer = CategoryValidateSerializer(
            data=request.data,
            context={'category_id': category.id}
        )

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        category.name = validate_serializer.validated_data.get('name')
        category.save()

        data = CategorySerializer(category, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    elif request.method == 'DELETE':
        category.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        validate_serializer = ProductValidateSerializer(data=request.data)

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = validate_serializer.validated_data

        product = Product.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            price=validated_data.get('price'),
            category_id=validated_data.get('category_id')
        )

        data = ProductSerializer(product, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            data='Product not found!',
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = ProductSerializer(product, many=False).data

        return Response(data=data)

    elif request.method == 'PUT':
        validate_serializer = ProductValidateSerializer(data=request.data)

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = validate_serializer.validated_data

        product.title = validated_data.get('title')
        product.description = validated_data.get('description')
        product.price = validated_data.get('price')
        product.category_id = validated_data.get('category_id')
        product.save()

        data = ProductSerializer(product, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    elif request.method == 'DELETE':
        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(reviews, many=True).data

        return Response(data=data)

    elif request.method == 'POST':
        validate_serializer = ReviewValidateSerializer(data=request.data)

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = validate_serializer.validated_data

        review = Review.objects.create(
            text=validated_data.get('text'),
            product_id=validated_data.get('product_id'),
            stars=validated_data.get('stars')
        )

        data = ReviewSerializer(review, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(
            data='Review not found!',
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        data = ReviewSerializer(review, many=False).data

        return Response(data=data)

    elif request.method == 'PUT':
        validate_serializer = ReviewValidateSerializer(data=request.data)

        if not validate_serializer.is_valid():
            return Response(
                data=validate_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = validate_serializer.validated_data

        review.text = validated_data.get('text')
        review.product_id = validated_data.get('product_id')
        review.stars = validated_data.get('stars')
        review.save()

        data = ReviewSerializer(review, many=False).data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    elif request.method == 'DELETE':
        review.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.prefetch_related('reviews').all()

    data = ProductReviewsSerializer(products, many=True).data

    return Response(data=data)
