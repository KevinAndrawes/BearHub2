# Generated by Django 4.1.6 on 2023-02-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=64)),
                ('Last_name', models.CharField(max_length=64)),
                ('grade_level', models.IntegerField()),
                ('password', models.CharField(max_length=64)),
            ],
        ),
    ]
