from django.http import HttpResponse
from django.db import DatabaseError
from django.core.cache import cache

# Create your views here.


def health_check(request):
    try:
        # Check database connectivity
        # You might want to execute a simple read operation here
        # ...

        # Check cache
        cache.set('health_check', 'ok', timeout=30)
        if cache.get('health_check') != 'ok':
            raise ValueError("Cache not working")

        return HttpResponse("OK", content_type="text/plain")
    except (DatabaseError, ValueError) as e:
        return HttpResponse(str(e), status=500, content_type="text/plain")
