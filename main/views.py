from django.shortcuts import render
from django.db.models import Count
from services.models import Service
from django.contrib.auth import logout as django_logout


def home(request):
    # find the most popular services
    qs = (Service.objects
          .values('field')
          .annotate(num=Count('id'))
          .order_by('-num')[:4])
    
    # build a list of {name, slug} for the template
    top_categories = []
    for entry in qs:
        name = entry['field']
        slug = name.lower().replace(' ', '-')
        top_categories.append({'name': name, 'slug': slug})

    return render(request, "main/home.html", {
        'top_categories': top_categories
    })


def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")

def page_not_found(request, exception):
    return render(request, "errors/404.html", status=404)
