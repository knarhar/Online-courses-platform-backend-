# Generated by Django 5.0 on 2024-04-07 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_userprogress_completed_lectures_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprogress',
            name='completed_lectures',
            field=models.ManyToManyField(blank=True, null=True, related_name='completed_lecture_progress', to='api.lecture'),
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='completed_modules',
            field=models.ManyToManyField(blank=True, null=True, related_name='completed_module_progress', to='api.module'),
        ),
    ]
