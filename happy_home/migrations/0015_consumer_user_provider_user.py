# Generated by Django 4.2 on 2023-04-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('happy_home', '0014_rename_user_review_consumer'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumer',
            name='user',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='provider',
            name='user',
            field=models.IntegerField(null=True),
        ),
    ]
