# Generated by Django 2.0.1 on 2018-01-12 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180107_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='thread',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_conflict_participant',
            field=models.BooleanField(choices=[(True, 'Si'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_conflict_victim',
            field=models.BooleanField(choices=[(True, 'Si'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_living_in_conflict_zone',
            field=models.BooleanField(choices=[(True, 'Si'), (False, 'No')], default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(choices=[('Don', 'Don'), ('Doña', 'Doña'), ('Señor', 'Señor'), ('Señora', 'Señora'), ('Señorita', 'Señorita')], default='Don', max_length=50),
        ),
    ]
