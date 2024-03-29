# Generated by Django 3.2.6 on 2022-01-30 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0020_auto_20220121_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='solution',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='question',
            name='solutionImg',
            field=models.ImageField(blank=True, upload_to='photos'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
