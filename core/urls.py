from django.http import JsonResponse
from django.urls import include, path
from rest_framework import routers

from tasks.views import UserViewSet, GroupViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"tasks", TaskViewSet)

def health(request):
    return JsonResponse({"status": "ok"})

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('', include('django_prometheus.urls')),
]

PROMETHEUS_LATENCY_BUCKETS = (
    0.005,  # 5ms
    0.01,   # 10ms
    0.025,  # 25ms
    0.05,   # 50ms
    0.1,    # 100ms
    0.25,   # 250ms
    0.5,    # 500ms
    1.0,    # 1s
    2.5,    # 2.5s
    5.0,    # 5s
    7.5,
    10.0,   # 10s
    15.0,   # 15s
    25.0,
    50.0,   # 50s
    75.0,
    float('inf'),
)