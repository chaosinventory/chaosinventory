# Generated by Django 3.1.6 on 2021-02-08 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatype',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='inventoryidschema',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='inventory_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='base.iteminventoryid'),
        ),
        migrations.AlterField(
            model_name='item',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='location',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
        migrations.AlterField(
            model_name='overlay',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='inventory_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='base.productinventoryid'),
        ),
        migrations.AlterField(
            model_name='product',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='base.Tag'),
        ),
    ]
