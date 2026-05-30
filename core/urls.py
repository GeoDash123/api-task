from django.http import JsonResponse
from django.urls import include, path

from rest_framework import routers

from tasks.views import GroupViewSet, TaskViewSet, UserViewSet


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"tasks", TaskViewSet)


def health(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("django_prometheus.urls")),
]

PROMETHEUS_LATENCY_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.1,
    0.25,
    0.5,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    15.0,
    25.0,
    50.0,
    75.0,
    float("inf"),
)
