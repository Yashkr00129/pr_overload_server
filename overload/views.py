from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Exercise, Split, Set, Workout, User
from .serializers import ExerciseSerializer, SplitSerializer, SetSerializer, WorkoutSerializer, CreateWorkoutSerializer, \
    UserSerializer, UserCreateSerializer


# Create your views here.
class UserViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_context(self):
       return {"user": self.request.user}
    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class ExerciseViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [IsAuthenticated]
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()


class SplitViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = SplitSerializer
    queryset = Split.objects.all()


class SetViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = SetSerializer
    queryset = Set.objects.all()


class WorkoutViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = WorkoutSerializer
    queryset = Workout.objects.all()

    def get_serializer_context(self):
        print(self.request.user)

        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateWorkoutSerializer
        else:
            return WorkoutSerializer
