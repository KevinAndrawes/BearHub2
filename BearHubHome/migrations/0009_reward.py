# Generated by Django 4.1.6 on 2023-03-16 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BearHubHome', '0008_eventrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64)),
                ('point_value', models.IntegerField()),
            ],
        ),
    ]
