from django.views.static import serve
from django.http import FileResponse
from django.shortcuts import render
from pathlib import Path

def index(request):
    return render(request, 'base/index.html')

def app(request, path, document_root=None):
    if path.startswith("assets/"):
        return serve(request, path, document_root=document_root)

    fullpath = Path(document_root) / 'index.html'
    response = FileResponse(fullpath.open('rb'), content_type='text/html')
    return response
