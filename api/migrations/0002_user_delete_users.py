# Generated by Django 5.0.6 on 2024-07-10 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=56)),
                ('last_name', models.CharField(max_length=56)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='Users',
        ),
    ]
