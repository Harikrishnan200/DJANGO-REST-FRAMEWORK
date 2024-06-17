from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person,Team
from .serializer import PersonSerializer,RegisterSerializer,LoginSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Create your views here.


# here we use APIView method (can use any other method)
class RegisterAPI(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)  # create an instance for RegisterSerializer class
        # this serializer returns data which may be either valid or invalid

        if not serializer.is_valid():  # when we call serializer.is_valid() actually validate fn in RegisterSerializer class ( in serializer.py ) actually works
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()        # when we call serializer.save() actually create fn in RegisterSerializer class ( in serializer.py ) actually works

        return Response({'message':'User created Successfilly'}, status=status.HTTP_201_CREATED)

class CreateLoginAPI(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=serializer.data['username'],password=serializer.data['password'])

        if not user:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token,value = Token.objects.get_or_create(user=user)  # value is a boolean variable , get_or_create fn actually returns two values
        return Response({"message":"Login Successfully","token":str(token)}, status=status.HTTP_201_CREATED)




@api_view(['GET','POST'])
def index(request):
    if request.method == 'GET':
        people = {
            "name":"hari",
            "age": 25,  
            "city": "bangalore"
        }
        return Response(people)
    elif request.method == 'POST':
        return Response({"message": "This is a POST request"})  
    
    else:
        return Response({"message": "No data"})
    


@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
       # personobj = Person.objects.all()
        personobj = Person.objects.filter(team__isnull=False)  # to filter only the records thats team field value is not null  (team is a field name in Person model)
        serializer = PersonSerializer(personobj, many =True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        date = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
           # message = {'data':serializer.data, "success":True}
            return Response(serializer.data)
          #  return Response(message)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'PUT':  #  PUT method is for update a record completely
        data = request.data
        personobj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(personobj, data=data, partial = False)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == 'PATCH':    #  PATCH method is for partial update of a record 
        data = request.data
        personobj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(personobj, data=data, partial = True) # data=data update the existing data with the new data in request.data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    elif request.method == 'DELETE':
        data = request.data
        personobj = Person.objects.get(id=data['id'])
        personobj.delete()
        return Response({"message": "Record deleted successfully"})
    
    else:
        return Response({"message": "Invalid request method"})
        

@api_view(['GET', 'POST'])
def addPerson(request, pk):
    if request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'GET':
       # personobj = Person.objects.get(id=pk)
        personobj = get_object_or_404(Person, id=pk)
        serobj = PersonSerializer(personobj)
        return Response(serobj.data)
    
    return Response({"detail": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['PATCH'])
def editPerson(request,pk):
    if request.method == 'PATCH':
        data = request.data
        personobj = Person.objects.get(id=pk)
        serobj = PersonSerializer(personobj, data=data, partial = True)
        if serobj.is_valid():   
            serobj.save()
            return Response(serobj.data,status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
    
@api_view(['DELETE'])
def deletePerson(request, pk):
    if request.method == 'DELETE':
        """
        try:
            personobj = Person.objects.get(id=pk)
        except Person.DoesNotExist:
            return Response({"message": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
        
        personobj.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_200_OK)

    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    """
        personobj = get_object_or_404(Person, id=pk)
        personobj.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
   
