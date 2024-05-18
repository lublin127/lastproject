from django.db.models import Model, DecimalField, CharField, DateField, ImageField, PositiveIntegerField, TextField, EmailField, IntegerField, AutoField, ForeignKey, CASCADE
from django.core.validators import MinLengthValidator, MaxLengthValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.db.models import IntegerChoices
from django.utils.timezone import now
from rest_framework.serializers import ModelSerializer, SerializerMethodField

class RoleModel(IntegerChoices):
    Admin = 8, 'Admin'
    User = 9, 'User'
        
class UserModel(Model):
    first_name = CharField(max_length=20, validators=[MinLengthValidator(2), MaxLengthValidator(20)])
    last_name = CharField(max_length=30, validators=[MinLengthValidator(2), MaxLengthValidator(30)])
    email = EmailField(validators=[EmailValidator(), MinLengthValidator(5), MaxLengthValidator(100)])
    password = CharField(max_length=100, validators=[MinLengthValidator(4), MaxLengthValidator(100)])
    role = IntegerField(choices=RoleModel.choices)

    def clean(self):
        if not self.role in [RoleModel.Admin, RoleModel.User]:
            raise ValidationError({'role': 'Role must be User or Admin.'})
        
    class Meta:
        db_table = 'users'


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



    def clean(self):
        if self.start_date < now().date():
            raise ValidationError({'start_date': 'Start date cannot be in the past.'})
        if self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be earlier than the start date.'})
        if not self.price or self.price < 0 or self.price > 10000:
            raise ValidationError({'price': 'Price must be between 0 and 10,000.'})
        if len(self.vacation_description) < 2 or len(self.vacation_description) > 1000:
            raise ValidationError({'vacation_description': 'Description must be 2-1000 characters.'})
        if not self.image_file_name:
            raise ValidationError({'image': 'Please upload an image.'})
        
        
    
    class Meta:
        db_table = 'vacations'


class CredentialsModel(Model):

    email = EmailField(validators=[MinLengthValidator(5), MaxLengthValidator(100)])
    password = CharField(max_length=100, validators=[MinLengthValidator(4), MaxLengthValidator(100)])

    def validate(self):
        # Validate the email and password fields using Django's built-in functionality
        try:
            EmailValidator()(self.email)
        except ValidationError as e:
            return f"Email not valid: {e}"

        # Django models automatically call full_clean() to run validators before saving,
        # which would include our custom MinLengthValidator and MaxLengthValidator.
        # If you want to manually validate in your method, you can call full_clean() like this:
        try:
            self.full_clean()
        except ValidationError as e:
            return e.messages

        return None

    def __str__(self):
        return self.email


class VacationSerializer(ModelSerializer):
    country_name = SerializerMethodField()

    class Meta:
        model = VacationsModel  
        fields = ['vacation_id', 'country_name', 'vacation_description', 'start_date', 'end_date', 'price', 'image_file_name']

    def get_country_name(self, obj):
        return obj.country.country  # Correctly accessing the related Country object


