# Generated by Django 3.2.3 on 2021-09-18 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theSmartChurch', '0003_alter_congregants_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congregants',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]