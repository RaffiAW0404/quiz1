# Generated by Django 3.2.6 on 2022-01-30 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0021_auto_20220130_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='topic',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
