from django.urls import path

from .views import AvailableLessonsList, ProductList, RegistrationForCourse

urlpatterns = [
    path('lessons/<int:pk>/', AvailableLessonsList.as_view()),
    path('products/', ProductList.as_view()),
    path('registration_for_cours/', RegistrationForCourse.as_view())

]