from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("",views.dashboard_view, name="dashboard_view" ),
]