from django.urls import path

from . import views


urlpatterns = [
    path('create-connection/', views.create_connection, name='create-connection')

]