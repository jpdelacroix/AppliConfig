# Generated by Django 2.0.4 on 2019-01-25 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppliConfig', '0018_auto_20190125_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='vitapi',
            name='ligne',
            field=models.IntegerField(default=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vitapi',
            name='niveau',
            field=models.IntegerField(default=100),
            preserve_default=False,
        ),
    ]