# Generated by Django 2.2.10 on 2021-09-07 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20210907_1413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='variant',
        ),
        migrations.AddField(
            model_name='choice',
            name='variant',
            field=models.ManyToManyField(to='survey.Variant'),
        ),
    ]
