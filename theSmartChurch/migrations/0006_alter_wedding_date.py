# Generated by Django 3.2.3 on 2021-09-18 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theSmartChurch', '0005_alter_wedding_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wedding',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]