# Generated by Django 4.1.2 on 2022-11-16 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locator', '0009_alter_post_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
        migrations.AddField(
            model_name='post',
            name='found',
            field=models.BooleanField(default=False),
        ),
    ]
