from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello")

def api_files_list(request):
    return HttpResponse("World")

def api_files_details(request, uuid):
    return HttpResponse("File:"+uuid)
