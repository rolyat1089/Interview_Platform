# Generated by Django 3.2.3 on 2022-02-17 01:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewTest',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('DisplayTime', models.DateTimeField(blank=True)),
                ('EndTime', models.DateTimeField(blank=True)),
                ('Title', models.CharField(max_length=300)),
                ('Instructions', models.TextField(default=' ')),
                ('TestTime', models.IntegerField(default=0)),
                ('TestImage', models.URLField(default=' ')),
                ('accounts', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterViewQuestions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('QuestionName', models.CharField(default='', max_length=10)),
                ('Question', models.TextField(default='')),
                ('QuestionReadTime', models.IntegerField(default=0)),
                ('QuestionRecordTime', models.IntegerField(default=0)),
                ('MaxMarks', models.FloatField(default=0)),
                ('Test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='interviewQuiz.interviewtest')),
            ],
        ),
        migrations.CreateModel(
            name='InterviewTestAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartTime', models.DateTimeField(auto_now_add=True)),
                ('Attempted', models.BooleanField(default=False)),
                ('Finished', models.BooleanField(default=False)),
                ('Test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviewQuiz.interviewtest')),
                ('accounts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('Test', 'accounts')},
            },
        ),
        migrations.CreateModel(
            name='InterviewQuestionAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StartTime', models.DateTimeField(auto_now_add=True)),
                ('RecordStartTime', models.DateTimeField(null=True)),
                ('RecordAttempted', models.BooleanField(default=False)),
                ('Question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interviewQuiz.interviewquestions')),
                ('accounts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('Question', 'accounts')},
            },
        ),
    ]
