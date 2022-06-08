from django.urls import path

from . import views


urlpatterns = [
    path('import-cluster/', views.import_cluster, name='import-cluster'),
    path('get-cluster-api/', views.get_cluster_api, name='get-cluster-api')

]