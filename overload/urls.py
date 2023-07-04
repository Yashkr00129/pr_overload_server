from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register("users",views.UserViewSet, basename="users")
router.register('exercises', views.ExerciseViewSet, basename="exercises")
router.register('splits', views.SplitViewSet, basename="splits")
router.register('sets', views.SetViewSet, basename="sets")
router.register("workouts", views.WorkoutViewSet, basename="workouts")

urlpatterns = router.urls
