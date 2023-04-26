# Generated by Django 4.2 on 2023-04-25 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('happy_home', '0016_alter_review_consumer_alter_review_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(default='', max_length=1000)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='happy_home.review')),
            ],
            options={
                'verbose_name': 'Reply',
                'verbose_name_plural': 'Replies',
            },
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]