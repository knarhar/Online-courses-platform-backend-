# Generated by Django 5.0 on 2024-05-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_moduleprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprogress',
            name='quiz_results',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='ModuleProgress',
        ),
    ]