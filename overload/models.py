from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)


class Exercise(models.Model):
    TYPE_COMPOUND = "C"
    TYPE_ISOLATION = "I"
    TYPE_CHOICES = [
        (TYPE_COMPOUND, "Compound"),
        (TYPE_ISOLATION, "Isolation")
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_ISOLATION)

    # Add any other fields you want for your exercise model here


class Set(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.FloatField()
    reps = models.PositiveIntegerField()
    # Add any other fields you want for your set model here


class Split(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workouts = models.ManyToManyField('Workout')

    def __str__(self):
        return self.name

    def clean(self):
        if self.workouts.count() > 7:
            raise ValidationError('A split can have maximum 7 workouts')


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercises = models.ManyToManyField(Exercise)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SplitWorkout(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday')
    ]
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    workout = models.OneToOneField(Workout, on_delete=models.PROTECT)
