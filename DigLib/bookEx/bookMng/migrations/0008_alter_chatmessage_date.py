# Generated by Django 3.2.9 on 2021-12-06 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0007_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessage',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]