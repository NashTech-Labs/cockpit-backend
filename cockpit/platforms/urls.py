from django.urls import path

from . import views


urlpatterns = [
    path('create-platform/', views.create_platform_request, name='create-platform')

]