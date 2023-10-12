from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Exercise, Set, Workout, Profile, WorkoutExercise
from .serializers import ExerciseSerializer, SetSerializer, WorkoutSerializer, CreateWorkoutSerializer, \
    ProfileSerializer, CreateProfileSerializer, WorkoutExerciseSerializer, CreateWorkoutExerciseSerializer


# Create your views here.
class ProfileViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateProfileSerializer
        return ProfileSerializer


class ExerciseViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.request.method in ['GET']:
            return []
        return [IsAuthenticated()]

    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()


class SetViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = SetSerializer
    queryset = Set.objects.all()

    def get_serializer_context(self):
        return {
            'user': self.request.user,
            "workout_id": self.kwargs["workout_pk"],
            "workout_exercise_id":self.kwargs["workout_exercise_pk"]
        }

    def get_queryset(self):
        return Set.objects.filter(workout_exercise_id=self.kwargs["workout_exercise_pk"])


#     Here we want to get the sets
#     We also want to be able to add set to a workout


class WorkoutViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    queryset = Workout.objects.all()

    def get_serializer_context(self):
        return {'user': self.request.user}

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateWorkoutSerializer
        else:
            return WorkoutSerializer


class WorkoutExerciseViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    queryset = WorkoutExercise.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateWorkoutExerciseSerializer
        else:
            return WorkoutExerciseSerializer

    def get_queryset(self):
        return WorkoutExercise.objects.filter(workout_id=self.kwargs["workout_pk"])

    def get_serializer_context(self):
        return {
            'user': self.request.user,
            "workout_id": self.kwargs["workout_pk"]
        }
