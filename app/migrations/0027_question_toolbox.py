# Generated by Django 2.0.1 on 2018-02-16 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_question_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='toolbox',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Toolbox'),
        ),
    ]
