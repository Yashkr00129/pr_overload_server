from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("profiles", views.ProfileViewSet, basename="profiles")
router.register('exercises', views.ExerciseViewSet, basename="exercises")
router.register('sets', views.SetViewSet, basename="sets")
router.register("workouts", views.WorkoutViewSet, basename="workouts")

workout_router = routers.NestedDefaultRouter(router, 'workouts', lookup="workout")
workout_router.register("exercises", views.WorkoutExerciseViewSet, basename="workout-exercises")

workout_exercise_router = routers.NestedDefaultRouter(workout_router, "exercises", lookup="workout_exercise")
workout_exercise_router.register("sets", views.SetViewSet, basename="sets")

urlpatterns = router.urls + workout_router.urls + workout_exercise_router.urls
