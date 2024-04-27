# Generated by Django 5.0.4 on 2024-04-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_alter_review_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Health Tips', 'Health Tips'), ('Medication Updates', 'Medication Updates'), ('Disease Awareness', 'Disease Awareness'), ('Research and Development', 'Research and Development'), ('Wellness and Fitness', 'Wellness and Fitness')], max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]