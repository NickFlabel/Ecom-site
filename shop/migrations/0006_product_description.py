# Generated by Django 3.2.5 on 2022-06-01 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20220601_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='Here be descriptions'),
        ),
    ]