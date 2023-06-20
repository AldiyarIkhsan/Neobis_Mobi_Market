# Generated by Django 3.2.13 on 2023-06-20 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
