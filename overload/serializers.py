from rest_framework import serializers

from .models import Exercise, Split, Set, Workout, User


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name", "type"]


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ["id", "exercise", "reps", "weight"]


class SplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = ["id", "name"]


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = Workout
        fields = ["id", "name", "exercises"]


class CreateWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "name", "exercises"]

    def create(self, validated_data):
        # Add the user to the validated_data dictionary
        context_user = self.context["user"]
        user = User.objects.get(user_id=context_user.id)

        validated_data["user"] = user
        exercises = validated_data.pop("exercises")
        workout = Workout.objects.create(**validated_data)
        for exercise in exercises:
            workout.exercises.add(exercise)
        return workout


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "height", "weight")


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "height", "weight")

    def create(self, validated_data):
        #   Get the user from the context
        user = self.context["user"]
        validated_data["user"] = user

        # Create a user
        user = User.objects.create(**validated_data)
        return user
