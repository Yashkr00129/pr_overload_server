from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Exercise, Set, Workout, Profile, WorkoutExercise
from .serializers import AdminExerciseSerializer, SetSerializer, WorkoutSerializer, CreateWorkoutSerializer, \
    ProfileSerializer, CreateProfileSerializer, WorkoutExerciseSerializer, CreateWorkoutExerciseSerializer, \
    ExerciseSerializer


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

    serializer_class = AdminExerciseSerializer

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminExerciseSerializer
        else:
            return ExerciseSerializer

    def get_queryset(self):
        user = self.request.user.id
        profile = Profile.objects.get(user=user)
        return Exercise.objects.filter(Q(user=profile) | Q(user=None))


class SetViewSet(ModelViewSet):
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = SetSerializer
    queryset = Set.objects.all()

    def get_serializer_context(self):
        return {
            'user': self.request.user,
            "workout_id": self.kwargs["workout_pk"],
            "workout_exercise_id": self.kwargs["workout_exercise_pk"]
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

    # queryset = WorkoutExercise.objects.prefetch_related("set").all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateWorkoutExerciseSerializer
        else:
            return WorkoutExerciseSerializer

    # def get_queryset(self):
    #     return WorkoutExercise.objects.filter(workout_id=self.kwargs["workout_pk"]).prefetch_related("set_set")
    def get_queryset(self):
        return WorkoutExercise.objects.filter(workout_id=self.kwargs["workout_pk"]).prefetch_related('sets').all()

    def get_serializer_context(self):
        return {
            'user': self.request.user,
            "workout_id": self.kwargs["workout_pk"]
        }
