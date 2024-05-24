from django.db.models import Model, DecimalField, CharField, DateField, ImageField, PositiveIntegerField, TextField, EmailField, IntegerField, AutoField, ForeignKey, CASCADE
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db.models import IntegerChoices
from django.utils.timezone import now
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from enum import Enum


# ---------------------------------------------------------

class RoleModel(IntegerChoices):
    Admin = 8, 'Admin'
    User = 9, 'User'

# ---------------------------------------------------------
        

class UserModel(Model):
    user_id = AutoField(primary_key=True)
    first_name = CharField(max_length=20)
    last_name = CharField(max_length=30)
    email = EmailField(max_length=100)
    password = CharField(max_length=100)
    role_id = IntegerField()

    class Meta:
        db_table = 'users'

# Define the User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
        
# Define the Total users model
class TotalUsers(Model):
    total_users = IntegerField(default=0)
            
# Define the User serializer for the count of total users
class UserCountSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()

    

# ---------------------------------------------------------



class Country(Model):
    country_id = AutoField(primary_key=True)  # Explicit primary key definition
    country = CharField(max_length=255, unique=True, db_column='country')

    class Meta:
        db_table = 'countries'


    def __str__(self):
        return self.country

class VacationsModel(Model):
    vacation_id = AutoField(primary_key=True)
    country = ForeignKey(Country, on_delete=CASCADE, db_column='country_id')  # Make sure this matches the primary key column in the countries table.
    vacation_description = TextField(max_length=1000, validators=[MaxLengthValidator(1000),MinLengthValidator(2)])
    start_date = DateField()
    end_date = DateField()
    price = DecimalField(max_digits=10, decimal_places=2)
    image_file_name = ImageField(upload_to='static/images/vacations')

    
    class Meta:
        db_table = 'vacations'

class VacationSerializer(ModelSerializer):
    country_name = SerializerMethodField()

    class Meta:
        model = VacationsModel  
        fields = ['vacation_id', 'country_name', 'vacation_description', 'start_date', 'end_date', 'price', 'image_file_name']

    def get_country_name(self, obj):
        return obj.country.country  # Correctly accessing the related Country object
    
class VacationStatsSerializer(serializers.Serializer):
    past_vacations = serializers.IntegerField()
    on_going_vacations = serializers.IntegerField()
    future_vacations = serializers.IntegerField()
    

# ---------------------------------------------------------

# Define the Like model
class Like(Model):
    user_id = IntegerField()
    vacation_id = IntegerField()
    
    # specify the name of the database table for this model
    class Meta:
        db_table = 'likes'

# Define the Like serializer
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user_id', 'vacation_id']

# # Define the Total Likes model
# class TotalLikes(models.Model):
#     total_likes = models.IntegerField(default=0)
    
# Define the TotalLikes serializer     
class TotalLikesSerializer(serializers.Serializer):
        total_likes = serializers.IntegerField()
        
# Define the LikeDistribution serializer     
class LikeDistributionSerializer(serializers.Serializer):
        destination = serializers.CharField()
        likes = serializers.IntegerField()





