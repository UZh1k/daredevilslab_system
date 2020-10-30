from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Skipping)

# Register your models here.
