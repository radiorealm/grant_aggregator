from django.shortcuts import render
from . import database

def index(request):
    return render(request, 'grants/index.html')

def search(request):
    query = request.GET.get('q', '')
    results = database.search_grants(query) if query else []
    return render(request, 'grants/results.html', {'results': results, 'query': query})

def detail(request, grant_id):
    grant = database.get_grant_by_id(grant_id)
    if not grant:
        return render(request, 'grants/detail.html', {'error': 'Grant not found'})

    keys = ['id', 'site', 'name', 'country', 'grantor', 'facts']
    query = request.GET.get('q', '')
    return render(request, 'grants/detail.html', {
        'grant': dict(zip(keys, grant)),
        'query': query
    })

