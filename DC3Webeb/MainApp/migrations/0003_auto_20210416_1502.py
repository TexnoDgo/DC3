# Generated by Django 3.2 on 2021-04-16 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_auto_20210416_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MainApp.info', unique=True),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='code',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='storageplace',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
