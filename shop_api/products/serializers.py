from rest_framework import serializers

from .models import Category, Product, Review



class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ('id', 'name', 'products_count')
        
    def get_products_count(self, category):
        return category.products.count()
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'description',
            'price',
            'category',
            'reviews',
            'rating',
        )

    def get_rating(self, product):
        reviews = product.reviews.all()

        if not reviews:
            return 0

        total_stars = sum(review.stars for review in reviews)
        return round(total_stars / len(reviews), 1)


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=1, max_length=255)

    def validate_name(self, name):
        category_id = self.context.get('category_id')
        categories = Category.objects.filter(name=name)

        if category_id:
            categories = categories.exclude(id=category_id)

        if categories.exists():
            raise serializers.ValidationError('Category already exists!')

        return name


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=1, max_length=255)
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        default=''
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError('Category does not exist!')

        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=1)
    product_id = serializers.IntegerField()
    stars = serializers.IntegerField(
        min_value=1,
        max_value=5,
        default=5
    )

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist!')

        return product_id
