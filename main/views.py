from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import random


def index(request):
    print(request.GET.get('type'))
    print(request.GET.get('type') == 'get_random_project')
    if request.GET.get('type') == 'get_random_project':
        print('yes')
        projects = [
            reverse('books_project:books_perspective'),
            reverse('books_project:authors_perspective'),
            reverse('jobs_project:jobs'),
            reverse('netflix_project:netflix_titles'),
        ]
        return JsonResponse({'url': random.choice(projects)})
    
    return render(request, 'main/index.html')