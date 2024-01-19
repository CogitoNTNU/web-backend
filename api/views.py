from django.http import HttpResponse
from django.db import DatabaseError
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny

# Create your views here.


@swagger_auto_schema(
    method="GET",
    operation_description="Health check",
    tags=["Health"],
    responses={200: "OK"},
)
@permission_classes([AllowAny])
@api_view(["GET"])
def health_check(request):
    try:
        # Check database connectivity
        # You might want to execute a simple read operation here

        cache.set("health_check", "ok", timeout=30)
        if cache.get("health_check") != "ok":
            raise ValueError("Cache not working")

        return HttpResponse("OK", content_type="text/plain")
    except (DatabaseError, ValueError) as e:
        return HttpResponse(str(e), status=500, content_type="text/plain")
