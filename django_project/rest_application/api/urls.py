from django.urls import path

app_name = 'api-rest'

from . import views

urlpatterns = [
    path('profiles/', views.get_post_profile, name='get_post'),
    path('profiles/<int:pk>/', views.get_put_delete_profile, name='get_put_delete'),
]