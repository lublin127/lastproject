from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import VacationSerializer
from django.http import JsonResponse
from django.db import models
from api.models import VacationStatsSerializer, UserCountSerializer, TotalLikesSerializer, LikeDistributionSerializer, UserSerializer
from .models import VacationsModel, Country, UserModel, RoleModel, Like
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import login, logout
from .cyber import Cyber


@api_view(["GET", "POST"])
def get_vacations(request):
    if request.method == 'GET':
        try:
            vacations = VacationsModel.objects.all()
            serializer = VacationSerializer(vacations, many=True)
            return Response(serializer.data)
        except Exception as err:
            json = {"error": str(err)}
            return Response(json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'POST':
        serializer = VacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# --------------------------------------------------------------


@api_view(["GET"])
def get_vacation_stats(request):
    try:
        
        # Check if user actually logged-in:
        if ("is_logged-in" in request.session) == False:
            return Response({'error': 'You are not logged-in.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Calculation of the amount of vacations that have ended as of the current day
        past_vacations = VacationsModel.objects.filter(end_date__lt=timezone.now()).count()

        # Calculation of the amount of vacations that on-going on this current day 
        on_going_vacations = VacationsModel.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now()).count()

        #Calculation of the amount of future vacations
        future_vacations = VacationsModel.objects.filter(start_date__gt=timezone.now()).count()

        # Creating an object to return later with JSON : 
        vacations_stats_data = {
            "past_vacations": past_vacations,
            "on_going_vacations": on_going_vacations,
            "future_vacations": future_vacations
        }

        # create a serializer instance with the data
        # Convert the object data to a JSON formaא
        serializer = VacationStatsSerializer(vacations_stats_data)

        # print (1/0)
        # החזרת התוצאה בפורמט JSON
        return Response(serializer.data)
    
    except Exception as err: 
        # return an error response if an exception occurs
        json = { "error": str(err) }
        return Response (json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#----------------------------------------------------------#
@api_view(["GET"])
def get_total_likes(request):
    try: 
        
        # Check if user actually logged-in:
        if ("is_logged-in" in request.session) == False:
            return Response({'error': 'You are not logged-in.'}, status=status.HTTP_401_UNAUTHORIZED)
      
        # Count the amount of likes in all of the vacations
        total_likes = Like.objects.count()

        # Create a serializer instance with the total_likes data
        serializer = TotalLikesSerializer({"total_likes": total_likes})

        # Return the serialized data as a JSON response
        return Response(serializer.data)
    
    except Exception as err: 
        # return an error response if an exception occurs
        json = { "error": str(err) }
        return Response (json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#----------------------------------------------------------#
@api_view(["GET"])
def get_total_users(request):
    try:
        
        # Check if user actually logged-in:
        if ("is_logged-in" in request.session) == False:
            return Response({'error': 'You are not logged-in.'}, status=status.HTTP_401_UNAUTHORIZED)
       
        # Count the amount of users  registered in the database
        total_users = UserModel.objects.count()

        # Create a serializer instance with the total_users data
        serializer = UserCountSerializer({"total_users": total_users})

        # Return the serialized data as a JSON response
        return Response(serializer.data)
    
    except Exception as err: 
        # return an error response if an exception occurs
        json = { "error": str(err) }
        return Response (json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#----------------------------------------------------------#

@api_view(['GET'])
def get_likes_distribution(request):
    try: 
        # Check if user actually logged-in:
        if ("is_logged-in" in request.session) == False:
            return Response({'error': 'You are not logged-in.'}, status=status.HTTP_401_UNAUTHORIZED)
       
        # Get all vacation IDs and their respective countries
        vacations = VacationsModel.objects.values('vacation_id', 'country__country_name')

        # Initialize response data
        response_data = []

        # Iterate over vacations
        for vacation in vacations:
            # Count likes for the current vacation ID
            likes_count = Like.objects.filter(vacation_id=vacation['vacation_id']).count()

            # Append to response data
            response_data.append({
                # 'vacation_id': vacation['vacation_id'],
                'country': vacation['country__country_name'],
                'total_likes': likes_count
            })

        # Creating a collection that will include destination data and amount of likes for all vacations in this destination
        likes_per_country = {}

        # Iterate over the vacations data
        for vacation in response_data:
            # Get the country name and total likes for the current vacation
            country_name = vacation['country']
            total_likes = vacation['total_likes']
            
            # If the country already exists in the likes_per_country dictionary, add the total likes to the existing value
            if country_name in likes_per_country:
                likes_per_country[country_name] += total_likes
            
            # If the country doesn't exist in the dictionary, initialize it with the total likes
            else:
                likes_per_country[country_name] = total_likes

        # Convert the likes_per_country dictionary into a list of dictionaries, each containing 'country' and 'total_likes'
        likes_distribution = [{'destination': country, 'likes': likes} for country, likes in likes_per_country.items()]

        # Create a serializer instance with the likes_distribution
        serializer = LikeDistributionSerializer(likes_distribution, many=True)

        # Return the serialized data as a JSON response
        return Response(serializer.data)
    
    except Exception as err: 
        # return an error response if an exception occurs
        json = { "error": str(err) }
        return Response (json, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#----------------------------------------------------------#

@api_view(['POST'])
def log_in(request):
    try:
        if request.method == 'POST':
            email = request.data.get('email')
            password = request.data.get('password')

            # Checking if there is a user with this email
            user= UserModel.objects.get(email=email)
            
            # If there is no user with this Email
            if (user is None): 
                return Response({'error': 'Incorrect email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Changing the password by adding hash and salt    
            hashed_password = Cyber.hash(password)  
            
            # Check if the hashed_password matches the user - if not raise error 
            if hashed_password != user.password:
                return Response({'error': 'Incorrect email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Check if the User is Admin    
            if user.role_id != RoleModel.Admin.value:
                    return Response({'error': 'You are not authorized.'}, status=status.HTTP_403_FORBIDDEN)
                
            # login -  django order
            request.session["is_logged-in"] = True
            
            # Create a serializer instance with the user
            serializer = UserSerializer(user)
            return Response(serializer.data)
            
    except UserModel.DoesNotExist:
        return Response({ "error": "User Does Not Exist" }, status=status.HTTP_404_NOT_FOUND)
           
    except Exception as err:
        # return an error response if an exception occurs
        return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#----------------------------------------------------------#

# Logout view
@api_view(['POST'])
def log_out(request):
    try:
           
        # Clear session:
        request.session.flush()

        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    except Exception as err:
        return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
