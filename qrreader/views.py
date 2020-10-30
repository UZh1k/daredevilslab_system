from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound

website = '127.0.0.1:8000/'


def main(request):
    courses = Course.objects.all()
    users = User.objects.all()
    if not request.user.is_superuser:
        return redirect('/admin')
    if request.method == "POST":
        title = request.POST["title"]
        value = request.POST["value"]
        teacher = request.POST["teacher"]
        teacher = User.objects.get(username=teacher)
        course = Course.objects.create(title=title, value=value, teacher=teacher)
    return render(request, 'main.html', {'courses': courses,
                                         'users': users,
                                         })


def client_list(request):
    clients = Client.objects.all()
    courses = Course.objects.all()
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        course_id = request.POST["course"]
        course = Course.objects.get(id=course_id)
        last_client = Client.objects.latest('id')
        if request.POST["username"] == "":
            username = "user"+str(last_client.id+1)
        else:
            username = request.POST["username"]
        user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
        user.set_password("Grisha00")
        user.save()
        client = Client.objects.create(user=user)
        client.courses.add(course)
        client.save()

    return render(request, 'client_list.html', {'clients': clients,
                                                'courses': courses,
                                                })


def lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'lesson.html', {'lesson': lesson,
                                           'website': website,
                                           })


def course(request, course_id):
    course = Course.objects.get(id=course_id)
    clients = Client.objects.all()
    if request.method == "GET":
        try:
            lesson_id = request.GET['lesson_id']
            client_id = request.GET['client_id']
            lesson = Lesson.objects.get(id=lesson_id)
            client = Client.objects.get(id=client_id)
            if client in lesson.clients_came.all():
                lesson.clients_came.remove(client)
            else:
                lesson.clients_came.add(client)
            return render(request, 'course.html', {'course': course,
                                                   'clients': clients,
                                                   })
        except:
            return render(request, 'course.html', {'course': course,
                                                   'clients': clients,
                                                   })

    if request.method == "POST" and request.POST.get("form_type") == "add_lesson":
        print(request.POST)
        date = request.POST["date"]
        lesson = Lesson.objects.create(date=date, course=course)
        lesson.generate_url()
        lesson.save()

    if request.method == "POST" and request.POST.get("form_type") == "add_client":
        print(request.POST)
        client_id = request.POST["new_client"]
        client = Client.objects.get(id=client_id)
        course.client_set.add(client)
        course.save()

    return render(request, 'course.html', {'course': course,
                                           'clients': clients,
                                           })


def check_in(request, lesson_url):
    lesson = Lesson.objects.get(url=lesson_url)
    course = lesson.course
    user = request.user
    if user.is_authenticated:
        client = user.client
        lesson.clients_came.add(client)
        if client not in course.client_set.all():
            course.client_set.add(client)
        lesson.save()
        return render(request, 'success.html')
    else:
        return redirect('/' + lesson_url + '/login')


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
