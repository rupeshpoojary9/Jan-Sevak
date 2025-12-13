from django.urls import get_resolver
from django.conf import settings
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jan_sevak.settings')
django.setup()

def print_urls(resolver, prefix=''):
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'url_patterns'):
            print_urls(pattern, prefix + str(pattern.pattern))
        else:
            print(prefix + str(pattern.pattern))

print("Registered URLs:")
print_urls(get_resolver())
