# Generated by Django 3.2.5 on 2022-06-05 13:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0007_auto_20220605_1638'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerBonuses',
            new_name='Bonuses',
        ),
    ]