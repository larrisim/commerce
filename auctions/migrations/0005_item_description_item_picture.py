# Generated by Django 4.0.4 on 2022-05-30 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_categories_category_rename_items_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='picture',
            field=models.TextField(null=True),
        ),
    ]
