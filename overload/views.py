from rest_framework.viewsets import ModelViewSet

from .models import Exercise
from .serializers import ExerciseSerializer


# Create your views here.
class ExerciseViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
