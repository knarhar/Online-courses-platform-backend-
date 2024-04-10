# Generated by Django 5.0 on 2024-04-07 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_moduleprogress_module_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='quiz_results',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='completed_lectures',
            field=models.ManyToManyField(blank=True, related_name='completed_lecture_progress', to='api.lecture'),
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='completed_modules',
            field=models.ManyToManyField(blank=True, related_name='completed_module_progress', to='api.module'),
        ),
        migrations.AlterField(
            model_name='userprogress',
            name='completed_topics',
            field=models.ManyToManyField(blank=True, related_name='completed_topic_progress', to='api.topic'),
        ),
    ]
