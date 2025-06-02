from django.shortcuts import render
from . import database

def format_list_or_string(value):
    if isinstance(value, (list, tuple)):
        return ', '.join(str(item) for item in value)
    return str(value)

def index(request):
    query = request.GET.get('q', '')
    results = database.search_grants(query) if query else []
    return render(request, 'grants/index.html', {'results': results, 'query': query})

def detail(request, grant_id):
    grant = database.get_grant_by_id(grant_id)
    if not grant:
        return render(request, 'grants/detail.html', {'error': 'Грант не найден'})

    keys = ['id', 'site', 'name', 'country', 'grantor', 'facts']
    grant_dict = dict(zip(keys, grant))
    
    # Format country and facts if they're lists
    grant_dict['country'] = format_list_or_string(grant_dict['country'])
    grant_dict['facts'] = format_list_or_string(grant_dict['facts'])
    
    query = request.GET.get('q', '')
    return render(request, 'grants/detail.html', {
        'grant': grant_dict,
        'query': query
    })