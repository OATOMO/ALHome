# Generated by Django 2.1.3 on 2019-01-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATOM', '0003_auto_20190116_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(),
        ),
    ]
