# Generated by Django 3.2.6 on 2021-11-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0018_alter_question_diagram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='diagram',
            field=models.ImageField(blank=True, upload_to='photos'),
        ),
    ]
