
from django.urls import path
from home.views import index,person,addPerson,editPerson,deletePerson,RegisterAPI,CreateLoginAPI,user_list
from rest_framework.authtoken import views


urlpatterns = [
    path('index/', index, name='index'),
    path('person/', person, name='person'),
    path('addPerson/<int:pk>', addPerson, name='addPerson'),
    path('editPerson/<int:pk>', editPerson, name='editPerson'),
    path('deletePerson/<int:pk>', deletePerson, name='deletePerson'),
    path('register/', RegisterAPI.as_view(), name='register'),  # RegisterAPI is actually a class so we call it as view , so as_view() function is used
    path('userLogin/', CreateLoginAPI.as_view(), name='userLogin'),
    path('users/', user_list, name='user-list'),

    

]