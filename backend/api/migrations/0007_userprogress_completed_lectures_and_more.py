# Generated by Django 5.0 on 2024-04-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_userprogress_lecture_alter_userprogress_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='completed_lectures',
            field=models.ManyToManyField(related_name='completed_lecture_progress', to='api.lecture'),
        ),
        migrations.AddField(
            model_name='userprogress',
            name='completed_modules',
            field=models.ManyToManyField(related_name='completed_module_progress', to='api.module'),
        ),
    ]
