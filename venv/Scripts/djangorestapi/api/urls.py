
from django.urls import path
from home.views import index,person,addPerson,editPerson,deletePerson
urlpatterns = [
    path('index/', index, name='index'),
    path('person/', person, name='person'),
    path('addPerson/<int:pk>', addPerson, name='addPerson'),
    path('editPerson/<int:pk>', editPerson, name='editPerson'),
    path('deletePerson/<int:pk>', deletePerson, name='deletePerson'),
]