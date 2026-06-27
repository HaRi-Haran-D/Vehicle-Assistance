import os
import django
from django.urls import get_resolver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main_project.settings')
django.setup()

def show_urls(urllist, prefix=''):
    for entry in urllist:
        if hasattr(entry, 'url_patterns'):
            show_urls(entry.url_patterns, prefix + str(entry.pattern))
        else:
            print(prefix + str(entry.pattern))

show_urls(get_resolver().url_patterns)
