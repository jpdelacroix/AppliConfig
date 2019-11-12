# Generated by Django 2.0.4 on 2019-01-23 09:12

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('AppliConfig', '0007_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vimodel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='AppliConfig.Vimodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='company',
            name='parent',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]