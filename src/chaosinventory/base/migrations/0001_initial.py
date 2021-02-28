# Generated by Django 3.1.6 on 2021-02-28 12:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('part_of', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.entity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryIdSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('actual_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='actual_contents', to='base.item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('belongs_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.entity')),
                ('in_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.location')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Overlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
                ('active', models.BooleanField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='children', to='base.overlay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.tag')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventoryId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.product')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.inventoryidschema')),
            ],
        ),
        migrations.CreateModel(
            name='ProductData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.product')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.datatype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='base.Tag'),
        ),
        migrations.CreateModel(
            name='OverlayItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('overlay', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.overlay')),
                ('target_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='overlay_contents', to='base.item')),
                ('target_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='overlay_contents', to='base.location')),
            ],
        ),
        migrations.CreateModel(
            name='LocationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.location')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.datatype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='location',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='base.Tag'),
        ),
        migrations.CreateModel(
            name='ItemInventoryId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.inventoryidschema')),
            ],
        ),
        migrations.CreateModel(
            name='ItemData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.datatype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='actual_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='actual_contents', to='base.location'),
        ),
        migrations.AddField(
            model_name='item',
            name='belongs_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='base.entity'),
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.product'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='base.Tag'),
        ),
        migrations.AddField(
            model_name='item',
            name='target_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='target_contents', to='base.item'),
        ),
        migrations.AddField(
            model_name='item',
            name='target_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='target_contents', to='base.location'),
        ),
        migrations.CreateModel(
            name='EntityData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.entity')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='base.datatype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='entity',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='base.Tag'),
        ),
    ]
