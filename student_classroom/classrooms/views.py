from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from classrooms.models import Classrooms
# Create your views here.

def homePage(request):
    class_names = Classrooms.objects.all()
    data = {
        'name_list' : class_names,
    }
    return render(request, "Classroom.html", data)
