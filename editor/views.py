import base64
import json
import os

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render

@ensure_csrf_cookie
def index(request):    
    return render(request, 'editor/index.html')

def _create_directory_dict(path, basepath=None):
    if not basepath:
        basepath = path
    
    res = []
    for f in os.listdir(path):
        if f in ['node_modules', 'static', 'db.sqlite3', '__pycache__', 'source-to-set-path.py', 'package.json', 'package-lock.json', 'requirements.txt']: # TODO we need smarter rules here, as static is allowed as a subdir, but not a root dir
            continue
        if f.startswith('.') and not f in ['.gitignore',]:
            continue
        
        fullpath = os.path.join(path, f)
        uuid = str(base64.urlsafe_b64encode(fullpath[len(basepath)+1:].encode('utf-8')), 'utf-8')
        
        if os.path.isdir(fullpath):
            res.append({'label': f, 'uuid': uuid, 'children': _create_directory_dict(fullpath, basepath)})
        elif os.path.isfile(fullpath):
            res.append({'label': f, 'uuid': uuid})
    return res

def api_files_list(request):
    if request.method == 'GET':
        context = {}
        context['files'] = {'label': '/', 'uuid': '', 'children': _create_directory_dict(os.getcwd())}

        return HttpResponse(json.dumps(context, ensure_ascii=False))
    else:
        return HttpResponseNotAllowed(['GET'])

def api_files_details(request, uuid):
    return HttpResponse("File:"+uuid)
