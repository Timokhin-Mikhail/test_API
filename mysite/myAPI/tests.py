# Create your tests here.
from django.db.models import Prefetch

from .models import Lesson, Product

result = (Lesson.objects.prefetch_related(Prefetch('product', queryset=Product.objects.prefetch_related('students')))
          .filter(product__students__id=9))
print(result)
for i in result:
    print(i.__dict__)