from django.urls import path
from . import views

urlpatterns = [
    #POST http://localhost:8001/api/vacations
    path("vacations", views.get_vacations),

    # GET http://localhost:8000/api/vacations_stats
    path ("vacations_stats", views.get_vacation_stats), 
    
    # GET http://localhost:8000/api/total_likes 
    path ("total_likes", views.get_total_likes),
     
    # GET http://localhost:8000/api/total_users 
    path ("total_users", views.get_total_users), 
    
    # GET http://localhost:8000/api/likes_distribution 
    path ("likes_distribution", views.get_likes_distribution),
    
    #POST http://localhost:8000/api/login
    path ("login", views.log_in), 
    
    #POST http://localhost:8000/api/logout 
    path ("logout", views.log_out)
    
]