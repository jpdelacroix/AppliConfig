# Generated by Django 2.0.4 on 2019-01-25 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppliConfig', '0016_auto_20190125_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vitapi',
            name='clef',
        ),
        migrations.RemoveField(
            model_name='vitapi',
            name='ligne',
        ),
    ]
