# Generated by Django 3.2.6 on 2021-08-31 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_auto_20210831_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='QuizId',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
