# Generated by Django 3.1.6 on 2021-03-11 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitydata',
            name='value',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='itemdata',
            name='value',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='locationdata',
            name='value',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productdata',
            name='value',
            field=models.CharField(max_length=255),
        ),
    ]