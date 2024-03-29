# Generated by Django 2.0.1 on 2018-01-04 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='audio_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='img',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='comment',
            name='video_url',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='audio_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='img',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='thread',
            name='video_url',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
