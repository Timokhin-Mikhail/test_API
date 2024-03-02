from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200, blank=False, null=False, unique=True)
    start_date_time = models.CharField(max_length=100, default=datetime.now().strftime("%Y-%m-%d %H:%M"))
    price = models.IntegerField(default=0)
    min_stud_in_group = models.IntegerField(default=1)
    max_stud_in_group = models.IntegerField(default=1000)


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    lesson_name = models.CharField(max_length=200, blank=False, null=False)
    url_address = models.URLField(blank=False, null=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    available_products = models.ManyToManyField(Product, related_name='students', through="StudentOnProduct")


class StudentOnProduct(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductGroup(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='groups')
    students = models.ManyToManyField(Student, related_name='groups')
    group_name = models.CharField(max_length=200, blank=False, null=False, unique=True)


