from django.urls import path

from .views import AvailableLessonsList, ProductList, RegistrationForCourse

urlpatterns = [
    path('lessons/<int:student_id>/<int:product_id>/', AvailableLessonsList.as_view()),
    path('products/', ProductList.as_view()),
    path('registration_for_cours/', RegistrationForCourse.as_view())

]