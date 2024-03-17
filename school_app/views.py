from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Course, Student, Teacher

def home(request):
    courses = Course.objects.all()
    return render(request, 'school_app/index.html', {'courses': courses})

@login_required
def courses(request):
    courses = Course.objects.all()
    return render(request, 'school_app/courses.html', {'courses': courses})

@login_required
def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'school_app/teachers.html', {'teachers': teachers})

@login_required
def enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    student.courses.add(course)
    return redirect('school_app:courses')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('school_app:home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'school_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('school_app:login')

@login_required
def profile(request):
    student = Student.objects.get(user=request.user)
    courses = student.courses.all()
    return render(request, 'school_app/profile.html', {'courses': courses})