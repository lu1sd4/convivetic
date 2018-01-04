# Generated by Django 2.0.1 on 2018-01-04 22:25

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20180104_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='Experience content')),
                ('pub_date', models.DateField(default=datetime.date.today)),
                ('video_url', models.CharField(max_length=50, null=True)),
                ('audio_url', models.CharField(max_length=100, null=True)),
                ('img', models.ImageField(null=True, upload_to='uploads/')),
                ('status', models.CharField(choices=[('P', 'Pendiente'), ('A', 'Aprobado'), ('R', 'Rechazado')], default='R', max_length=20)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExperienceTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ThreadTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='thread',
            name='likes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='status',
            field=models.CharField(choices=[('P', 'Pendiente'), ('A', 'Aprobado'), ('R', 'Rechazado')], default='R', max_length=20),
        ),
        migrations.AddField(
            model_name='thread',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(to='app.ExperienceTag'),
        ),
        migrations.AddField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(to='app.ThreadTag'),
        ),
    ]
