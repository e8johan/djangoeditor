from django.urls import path

from . import views

app_name = 'editor'

urlpatterns = [
    path('', views.index, name='index'),
    
    path('api/files', views.api_files_list),
    path('api/files/<uuid>/', views.api_files_details),
]
