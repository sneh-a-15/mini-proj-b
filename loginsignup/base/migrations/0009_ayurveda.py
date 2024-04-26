# Generated by Django 5.0.3 on 2024-04-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_myorders_remove_orderitem_order_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ayurveda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('med_name', models.CharField(max_length=250)),
                ('med_image', models.ImageField(blank=True, null=True, upload_to='products')),
                ('med_price', models.IntegerField()),
                ('med_descripton', models.TextField()),
                ('med_exp', models.DateField()),
            ],
        ),
    ]
