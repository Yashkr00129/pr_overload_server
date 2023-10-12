from rest_framework import serializers

from .models import Exercise, Set, Workout, Profile, WorkoutExercise


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "user", "height", "weight")


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "height", "weight")

    def create(self, validated_data):
        #   Get the user from the context
        user = self.context["user"]
        validated_data["user"] = user

        # Create a user
        user = Profile.objects.create(**validated_data)
        return user


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ["id", "name", "type"]


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ["id", "reps", "weight"]

    def create(self, validated_data):
        workout_exercise_id = self.context["workout_exercise_id"]
        return Set.objects.create(workout_exercise_id=workout_exercise_id, **validated_data)


class WorkoutExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)
    exercise = ExerciseSerializer()

    class Meta:
        model = WorkoutExercise
        fields = ["id", "exercise", "sets", ]


class CreateWorkoutExerciseSerializer(serializers.ModelSerializer):
    sets = SetSerializer(many=True, read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = ["id", "exercise", "sets"]

    def create(self, validated_data):
        workout_id = self.context['workout_id']
        return WorkoutExercise.objects.create(workout_id=workout_id, **validated_data)


class WorkoutSerializer(serializers.ModelSerializer):
    exercises = serializers.SerializerMethodField()

    def get_exercises(self, product):
        exercises = WorkoutExercise.objects.filter(workout_id=product.id)
        serializer = WorkoutExerciseSerializer(exercises, many=True)
        return serializer.data

    class Meta:
        model = Workout
        fields = ["id", "name", "user", "exercises", "date_created"]


class CreateWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "name"]

    def create(self, validated_data):
        context_user = self.context["user"]
        user = Profile.objects.get(user=context_user)

        validated_data["user"] = user
        workout = Workout.objects.create(**validated_data)
        return workout
