from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('exercises', views.ExerciseViewSet, basename="exercises")

urlpatterns = router.urls
