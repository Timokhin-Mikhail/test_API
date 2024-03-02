from django.db.models import Prefetch
from rest_framework import serializers
from .models import Product, Lesson, StudentOnProduct, ProductGroup


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ['lesson_name', 'url_address']


class ProductListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField()
    start_date_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Product
        fields = ["product_name", "price", "start_date_time", "lessons_count"]


class StudentsSerializer(serializers.Serializer):

    student_id = serializers.IntegerField()
    available_products = serializers.IntegerField()

    def update(self, instance, validated_data):
        product = (Product.objects
                   .prefetch_related(Prefetch('groups', queryset=ProductGroup.objects.prefetch_related('students')))
                   .prefetch_related("students").get(pk=validated_data.get("available_products")))

        entrance = StudentOnProduct(student=instance, product=product)
        entrance.save()
        return instance