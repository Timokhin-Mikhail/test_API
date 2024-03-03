from rest_framework import generics
from django.db.models import Count, Prefetch
from .models import Product, Lesson, Student
from rest_framework.views import APIView
from .serializers import LessonsSerializer, ProductListSerializer, StudentsSerializer
from rest_framework.response import Response
from rest_framework import status


class AvailableLessonsList(generics.ListAPIView):
    serializer_class = LessonsSerializer

    def get_queryset(self):
        return (Lesson.objects.prefetch_related(
            Prefetch('product', queryset=Product.objects.prefetch_related('students')))
                .filter(product__id=self.kwargs['product_id'])
                &
                Lesson.objects.prefetch_related(
                    Prefetch('product', queryset=Product.objects.prefetch_related('students')))
                .filter(product__students__id=self.kwargs['student_id']))




class ProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related("lessons"). annotate(lessons_count=Count('lessons'))


class RegistrationForCourse(APIView):

    def post(self, request):
        student = Student.objects.select_related("user").get(pk=request.data["student_id"])
        serializer = StudentsSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

