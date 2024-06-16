from rest_framework import serializers
from .models import Person,Team
from django.contrib.auth.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    # To validate if the user is already existing or not
    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError({'username': 'Username already exists'})
            
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError({'email': 'email already exists'})
            
        return data
    
    # If the above function is ok the goes to create functiom
    # To create a new user
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data

        
class LoginSerializer(serializers.Serializer):   # LoginSerializer is just any name
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['team_name']  # other fields are ignored

class PersonSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)  # read_only=True in a serializer field ensures that the field is used only for serialization and is ignored during deserialization.
                                           # During deserialization (e.g., creating or updating a Person), team field will be ignored. If you try to update or create a Person with a team object, it will not affect the Person instance.
    team_info = serializers.SerializerMethodField()                                       
    class Meta:
        model = Person
        fields = '__all__'
        depth = 1   # to show all the fields (in the case of foreign key field)  
    
    def get_team_info(self,obj):
        return "extra serializer field"

    # OUTPUT OF THIS METHOD
 
    """
    {
        "id": 1,
        "team": {
            "team_name": "RED"
        },
        "team_info": "extra serializer field",     # for this extra field
        "name": "Hari",
        "age": 20,
        "location": "Pandalam"
    }
    """


    # for server side validation
    def validate(self, attrs):      # attrs  means attributes (just any name)
        spi_chars = r"!@#$%^&*(){}}[]|\\?"    # spi_chars = "!@#$%^&*(){}}[]|\\?"  (special characters)

        if any(char in spi_chars for char in attrs['name']):
            raise serializers.ValidationError({"name_error":"Name should not contain special characters"})
        if attrs['age'] < 18:
            raise serializers.ValidationError({'age_error': 'You must be at least 18 years old'})
        return attrs




































































































































































































































































