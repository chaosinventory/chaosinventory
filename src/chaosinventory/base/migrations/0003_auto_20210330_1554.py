# Generated by Django 3.1.6 on 2021-03-30 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210311_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='location',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
    ]
