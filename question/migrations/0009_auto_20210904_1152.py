# Generated by Django 3.2.6 on 2021-09-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_auto_20210901_1149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='qa',
            new_name='q1',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='qb',
            new_name='q2',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='qc',
            new_name='q3',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='qd',
            new_name='q4',
        ),
        migrations.AlterField(
            model_name='question',
            name='a',
            field=models.CharField(max_length=1),
        ),
    ]
