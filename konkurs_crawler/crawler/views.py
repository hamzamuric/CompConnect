from django.shortcuts import render
import json

def index(request):
    data = {}
    with open('../data.json', 'r') as f:
        data = json.load(f)
    context = {'data': data}
    return render(request, 'crawler/index.html', context)
