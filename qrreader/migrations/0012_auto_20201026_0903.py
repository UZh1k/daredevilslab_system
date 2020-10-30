# Generated by Django 3.1.1 on 2020-10-26 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qrreader', '0011_auto_20201026_0827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='teacher',
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_teached', to=settings.AUTH_USER_MODEL),
        ),
    ]
