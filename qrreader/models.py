from django.db import models
from django.contrib.auth.models import User
import random, string


class Course(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.title


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='clients')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, related_name='lessons')
    clients_came = models.ManyToManyField(Client, blank=True)
    url = models.CharField(max_length=10, null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    def generate_url(self):
        if self.url is None:
            letters_and_digits = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(letters_and_digits) for i in range(10)))
            self.url = result_str

# Create your models here.
