# Generated by Django 3.2.6 on 2021-08-30 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0002_auto_20210830_1849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='questionID',
        ),
        migrations.AddField(
            model_name='question',
            name='question',
            field=models.CharField(default='question', max_length=200),
            preserve_default=False,
        ),
    ]
