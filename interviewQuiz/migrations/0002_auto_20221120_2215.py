# Generated by Django 3.2.3 on 2022-11-20 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviewQuiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interviewquestions',
            name='Test',
        ),
        migrations.DeleteModel(
            name='InterviewQuestionAttempt',
        ),
        migrations.DeleteModel(
            name='InterViewQuestions',
        ),
    ]
