# Generated by Django 2.0.4 on 2019-01-25 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppliConfig', '0015_auto_20190125_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitapi',
            name='ligne',
            field=models.IntegerField(),
        ),
    ]
