from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound

website = '127.0.0.1:8000/'

def lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'lesson.html', {'lesson': lesson,
                                           'website': website,
                                           })

def course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == "GET":
        try:
            print(request.GET)
            lesson_id = request.GET['lesson_id']
            client_id = request.GET['client_id']
            lesson = Lesson.objects.get(id=lesson_id)
            client = Client.objects.get(id=client_id)
            if client in lesson.clients_came.all():
                lesson.clients_came.remove(client)
            else:
                lesson.clients_came.add(client)
            return render(request, 'course.html', {'course': course})
        except:
            return render(request, 'course.html', {'course': course})

    return render(request, 'course.html', {'course': course})

def check_in(request, lesson_url):
    lesson = Lesson.objects.get(url=lesson_url)
    user = request.user
    if user.is_authenticated:
        client = user.client
        lesson.clients_came.add(client)
        lesson.save()
        return render(request, 'success.html')
    else:
        return redirect('/'+lesson_url+'/login')

def sign_in(request, lesson_url):
    if request.method == 'POST':
        username = request.POST['username']
        user = authenticate(request, username=username, password='Grisha00')
        if user is not None:
            login(request, user)
            return redirect('/' + lesson_url)
        else:
            return HttpResponseNotFound('<h1>Error: No such user</h1>')

    return render(request, 'login.html')

# Create your views here.

