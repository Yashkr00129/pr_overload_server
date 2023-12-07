from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)


class Exercise(models.Model):
    TYPE_COMPOUND = "C"
    TYPE_ISOLATION = "I"
    TYPE_CHOICES = [
        (TYPE_COMPOUND, "Compound"),
        (TYPE_ISOLATION, "Isolation")
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=1, choices=TYPE_CHOICES, default=TYPE_ISOLATION)
    personal = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Set(models.Model):
    workout_exercise = models.ForeignKey(
        "WorkoutExercise", on_delete=models.CASCADE, related_name="sets")
    weight = models.FloatField()
    reps = models.PositiveIntegerField()


class WorkoutExercise(models.Model):
    workout = models.ForeignKey("Workout", on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)


class Workout(models.Model):
    name = models.CharField(max_length=255, null=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
