# Generated by Django 3.2.6 on 2022-01-30 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0022_alter_question_topic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='QuizId',
        ),
    ]
