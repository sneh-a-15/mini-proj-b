# Generated by Django 5.0.4 on 2024-04-29 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_review_ayurveda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='prescriptions/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
