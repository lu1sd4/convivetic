# Generated by Django 2.0.1 on 2018-02-15 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0015_auto_20180212_2057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toolbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ToolboxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('toolbox', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Toolbox')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AnswerUsr',
        ),
        migrations.RemoveField(
            model_name='guide',
            name='name',
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='content',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='question',
            name='correct_answer',
            field=models.CharField(default='TEMP_TEST', max_length=100),
        ),
        migrations.AddField(
            model_name='question',
            name='q_type',
            field=models.CharField(choices=[('TEMP_INTRO', 'TEMP_INTRO'), ('TEMP_TEST', 'TEMP_TEST'), ('TEMP_TEST_IMAGE', 'TEMP_TEST_IMAGE'), ('TEMP_TEXT', 'TEMP_TEXT'), ('TEMP_ACTIVITY', 'TEMP_ACTIVITY'), ('TEMP_TEST_MULTIPLE', 'TEMP_TEST_MULTIPLE'), ('TEMP_CROSSWORD', 'TEMP_CROSSWORD')], default='TEMP_TEST', max_length=20),
        ),
    ]
