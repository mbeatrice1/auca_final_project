# Generated by Django 3.2.3 on 2021-09-18 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theSmartChurch', '0002_give_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congregants',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
