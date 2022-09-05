from django.urls import path

from . import views


urlpatterns = [
    path('import-cluster/', views.import_cluster, name='import-cluster'),
    path('get-cluster-api/', views.get_cluster_api, name='get-cluster-api'),
    path('create-cluster-api/', views.create_cluster_api, name='create-cluster-api'),
    path('delete-cluster-api/', views.delete_cluster_api, name='delete-cluster-api'),
    path('update-cluster-api/', views.update_cluster_api, name='update-cluster-api'),
    path('list-clusters/', views.get_cluster_imported_list, name='list-clusters'),
    path('cluster-monitoring/',views.cluster_monitoring, name='cluster-monitoring'),
    path('get-k8s-object-sepcific-details/',views.get_k8s_object_sepcific_details,name='get-k8s-object-sepcific-details'),
    path('list-monitoring-clusters/', views.get_cluster_monitoring_list, name='list-monitoring-clusters')
]