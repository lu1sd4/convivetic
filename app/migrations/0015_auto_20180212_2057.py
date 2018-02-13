# Generated by Django 2.0.2 on 2018-02-13 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20180204_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='experience',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.ExperienceTag'),
        ),
        migrations.AlterField(
            model_name='thread',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.ThreadTag'),
        ),
    ]
