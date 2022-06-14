from django.urls import path

from . import views


urlpatterns = [
    path('import-cluster/', views.import_cluster, name='import-cluster'),
    path('get-cluster-api/', views.get_cluster_api, name='get-cluster-api'),
    path('create-cluster-api/', views.create_cluster_api, name='create-cluster-api'),
    path('delete-cluster-api/', views.delete_cluster_api, name='delete-cluster-api'),
    path('update-cluster-api/', views.update_cluster_api, name='update-cluster-api')
]