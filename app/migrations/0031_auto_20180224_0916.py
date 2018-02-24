# Generated by Django 2.0.1 on 2018-02-24 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_toolbox_guide_n'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='fill_answer',
            field=models.CharField(blank=True, default='', max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.CharField(default='', max_length=1500),
        ),
        migrations.AlterField(
            model_name='question',
            name='correct_answer',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='q_type',
            field=models.CharField(choices=[('TEMP_INTRO', 'TEMP_INTRO'), ('TEMP_TEST', 'TEMP_TEST'), ('TEMP_TEST_IMAGE', 'TEMP_TEST_IMAGE'), ('TEMP_TEXT', 'TEMP_TEXT'), ('TEMP_ACTIVITY', 'TEMP_ACTIVITY'), ('TEMP_TEST_MULTIPLE', 'TEMP_TEST_MULTIPLE'), ('TEMP_CROSSWORD', 'TEMP_CROSSWORD'), ('TEMP_FILL_THE_BLANKS', 'TEMP_FILL_THE_BLANKS')], default='TEMP_TEST', max_length=20),
        ),
    ]
