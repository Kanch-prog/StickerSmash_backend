# Generated by Django 5.0.7 on 2024-08-18 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sticker_app', '0003_sticker_category_sticker_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='image',
            field=models.ImageField(upload_to='stickers/'),
        ),
    ]
