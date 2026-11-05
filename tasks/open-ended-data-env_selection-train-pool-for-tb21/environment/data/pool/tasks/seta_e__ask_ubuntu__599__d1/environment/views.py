import sys
from django.http import JsonResponse
import django


def version_view(request):
    return JsonResponse({
        "python_version": sys.version,
        "django_version": django.get_version(),
    })
