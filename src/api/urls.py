from django.urls import path
from . import views

urlpatterns = [

    #POST http://localhost:8001/api/vacations
    path("vacations", views.get_vacations)
]