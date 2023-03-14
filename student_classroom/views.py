from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users.models import Users
from classes.models import Persons
from classes.views import homePage
from django.contrib.sessions.models import Session
from classes.models import Classrooms, Persons
from doubt.models import Doubts
from answer.models import Answers
from material.models import Material
from assignment.models import Assignment
from submission.models import Submission
# import requests
# Create your views here.

def loginpage(request):
    return render(request,"Login&Signup.html")

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        person = Users.objects.get(email=email)
        msg = ""
        if not person:
            msg = "Users not registered"
        else:
            if person.password == password:
                request.session['user_id'] = person.user_id
                request.session['role'] = person.role
                request.session['name'] = person.name
                return homePage(request)
                # return render(request,"Classroom.html", data)
            else:
                msg = "Password is Incorrect"
        return render(request,"Login&Signup.html", {'msg' : msg})


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        role = request.POST['role']
        password = request.POST['password']
        obj = Users(name=name, email=email, password=password, role=role)
        obj.save()
        data = {'email': email, 'password': password}
        return render(request,"Login&Signup.html", data)

def addclass(request):
    return render(request,"Joinclass.html")

def joinclass(request):
    name = ""
    user_id = 0
    if request.method == "POST":
        user_id = request.session['user_id']
        classroom_id = int(request.POST['class_id'])
        role = request.session['role']
        # name = request.POST['name']
        # user = Users(user_id=user_id, role=role)
        obj = Persons(user_id=Users(user_id), classroom_id=Classrooms(classroom_id), role=Users(user_id))
        obj.save()
    return homePage(request)

def StreamPage(request):
    data = {}
    if request.method == "POST":
        class_id = request.POST['class_id']
        class_name = request.POST['class_name']
        request.session['class_id'] = class_id
        request.session['class_name'] = class_name
        material_list = Material.objects.filter(classroom_id=class_id)
        assignment_list = Assignment.objects.filter(classroom_id=request.session['class_id'])
        data = {
            'material_list':material_list,
            'assignment_list':assignment_list,
        }
    return render(request, "Stream.html", data) 

def PeoplePage(request):
    people_lst = Persons.objects.filter(classroom_id = request.session['class_id'])
    unique = set()
    for i in people_lst:
        username = Users.objects.get(user_id=i.user_id.user_id)
        unique.add(username)
    data = {
        'people_list':unique
    }
    return render(request, "People.html", data)

def homePage(request):
    person = Persons.objects.filter(user_id=request.session['user_id'])
    lst = set()
    for i in person:
        class_no = i.classroom_id.classroom_id
        class_names = Classrooms.objects.get(classroom_id = class_no)
        lst.add(class_names)
    data = {
        # 'name' : name,
        'name_list' : lst,
    }
    return render(request, "Classroom.html", data)

def createClass(request):
    return render(request, "createClassroom.html")

def generateClassroom(request):
    if request.method == "POST":
        class_name = request.POST['class_name']
        obj = Classrooms(classroom_name=class_name)
        obj.save()
        user_id = request.session['user_id']
        cls = Classrooms.objects.get(classroom_name=class_name)
        class_id = cls.classroom_id
        obj = Persons(user_id=Users(user_id), classroom_id=Classrooms(class_id), role=Users(user_id))
        obj.save()
    return homePage(request)

def DoubtPage(request):
    class_id = request.session['class_id']
    doubt_list = Doubts.objects.filter(classroom_id=class_id)
    name_list = []
    for i in doubt_list:
        stu = Users.objects.get(user_id=i.user_id.user_id)
        name_list.append(stu.name)
    data = {
        'name_list':name_list,
        'doubt_list':doubt_list,
    }
    return render(request, "Doubt.html", data)

def askdoubt(request):
    if request.method == "POST":
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        question = request.POST['question']
        obj = Doubts(user_id=Users(user_id), classroom_id=Classrooms(class_id), question=question)
        obj.save()
    return DoubtPage(request)

def answerdoubt(request):
    if request.method == "POST":
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        doubt_id = request.POST['doubt_id']
        ans = request.POST['ans']
        obj = Answers(user_id=Users(user_id), classroom_id=Classrooms(class_id), doubt_id=Doubts(doubt_id), ans=ans)
        obj.save()
    return DoubtPage(request)

def viewanswers(request):
    data = {}
    if request.method == "POST":
        class_id = request.session['class_id']
        doubt_id = int(request.POST['doubt_id'])
        answer_list = Answers.objects.filter(classroom_id=class_id, doubt_id=doubt_id)
        doubt = Doubts.objects.get(doubt_id=doubt_id)
        data = {
            'question' : doubt.question,
            'answer_list':answer_list,
        }
    return render(request, "viewAnswers.html", data)

def uploadmaterial(request):
    return render(request, "uploadMaterial.html")

def storematerial(request):
    if request.method == "POST":
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        title = request.POST['material_title']
        mat = request.FILES['material']
        obj = Material(user_id=Users(user_id), classroom_id=Classrooms(class_id), material_title=title, study_material=mat)
        obj.save()
    return streamPage(request)

def streamPage(request):
    material_list = Material.objects.filter(classroom_id=request.session['class_id'])
    assignment_list = Assignment.objects.filter(classroom_id=request.session['class_id'])
    data = {
        'material_list':material_list,
        'assignment_list':assignment_list,
    }
    return render(request, "Stream.html", data)

def logout(request):
    del request.session['class_id']
    del request.session['user_id']
    del request.session['role']
    del request.session['class_name']
    del request.session['name']
    return render(request, "Login&Signup.html")

def uploadassignment(request):
    return render(request, "uploadAssignment.html")

def storeassignment(request):
    if request.method == "POST":
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        title = request.POST['assignment_title']
        deadline = request.POST['deadline']
        marks = request.POST['marks']
        assign = request.FILES['assignment']
        obj = Assignment(user_id=Users(user_id), classroom_id=Classrooms(class_id), deadline=deadline, max_marks=marks, assignment=assign, assignment_title=title)
        obj.save()
    return streamPage(request)

def openassignment(request):
    if request.method == "POST":
        assignment_id = request.POST['assignment_id']
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        rst = Submission.objects.filter(assignment_id=assignment_id, classroom_id=class_id, user_id=user_id)
        if rst:
            data = {
                'assignment': Assignment.objects.get(assignment_id=assignment_id),
                'submission': Submission.objects.get(assignment_id=assignment_id, classroom_id=class_id, user_id=user_id),
            }
        else:
             data = {
                'assignment': Assignment.objects.get(assignment_id=assignment_id),
            }
    return render(request, "viewAssignment.html", data)

def storesubmission(request):
    if request.method == "POST":
        class_id = request.session['class_id']
        user_id = request.session['user_id']
        sub = request.FILES['submission']
        assignment_id = request.POST['assignment_id']
        obj = Submission(user_id=Users(user_id), classroom_id=Classrooms(class_id), assignment_id=Assignment(assignment_id), work=sub)
        obj.save()
        data = {
            'assignment': Assignment.objects.get(assignment_id=assignment_id),
            'submission': Submission.objects.get(assignment_id=assignment_id, classroom_id=class_id, user_id=user_id),
        }
    return render(request, "viewAssignment.html", data)

def viewsubmissions(request):
    data = {}
    if request.method == "POST":
        class_id = request.session['class_id']
        assignment_id = request.POST['assignment_id']
        if Submission.objects.filter(classroom_id=class_id, assignment_id=assignment_id):
            obj = Assignment.objects.filter(assignment_id=assignment_id)[0]
            data = {
                'all_submissions':Submission.objects.filter(classroom_id=class_id, assignment_id=assignment_id),
                'marks':obj.max_marks,
            }
        else:
            data = {
                'all_submissions':"empty",
            }
    return render(request, "viewSubmissions.html", data)

def addmarks(request):
    data = {}
    if request.method == "POST":
        submission_id = request.POST['submission_id']
        marks = request.POST['marks']
        obj = Submission.objects.get(submission_id=submission_id)
        obj.marks_obtained = marks
        obj.save()
        class_id = request.session['class_id']
        assignment_id = request.POST['assign_id']
        all_submission = Submission.objects.filter(classroom_id=class_id, assignment_id=assignment_id)
        if all_submission:
            obj = Assignment.objects.get(assignment_id=assignment_id)
            data = {
                'all_submissions':all_submission,
                'marks':obj.max_marks,
            }
        else:
            data = {
                'all_submissions':"empty",
            }
    return render(request, "viewSubmissions.html", data)

def grade(request):
    data = {}
    class_id = request.session['class_id']
    all_assignment = Assignment.objects.filter(classroom_id=class_id)
    if len(all_assignment) > 0:
        data = {
            'all_assignment':all_assignment, 
        }
    else:
        data = {
            'all_assignment':"empty", 
        }
    return render(request, "Grade.html", data) 