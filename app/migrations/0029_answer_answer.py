# Generated by Django 2.0.1 on 2018-02-17 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_merge_20180215_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer',
            field=models.CharField(default='', max_length=600),
        ),
    ]
