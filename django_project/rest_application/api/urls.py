from django.urls import path
from . import views


app_name = "api-rest"

urlpatterns = [
    path("profiles/", views.get_post_profile, name="get_post"),
    path("profiles/<pk>/", views.get_put_delete_profile, name="get_put_delete"),
    path("contents/", views.download_csv, name="get_contents"),
]
