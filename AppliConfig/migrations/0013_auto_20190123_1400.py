# Generated by Django 2.0.4 on 2019-01-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppliConfig', '0012_vitapi_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vitapi',
            name='key',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
