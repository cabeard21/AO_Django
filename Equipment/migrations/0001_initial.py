# Generated by Django 3.0.8 on 2020-12-21 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('tier', models.IntegerField(default=4)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTypeSpec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec_bonus', models.IntegerField(default=0)),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemtypespec_itemtype', to='Equipment.ItemType')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_tier', models.IntegerField(default=4, verbose_name='Minimum Tier')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemtier_item', to='Equipment.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='item_itemtype', to='Equipment.ItemType'),
        ),
        migrations.CreateModel(
            name='EquipmentSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_name', models.CharField(max_length=100, unique=True)),
                ('items', models.ManyToManyField(to='Equipment.ItemTier')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_name', models.CharField(max_length=100, unique=True)),
                ('mastery', models.ManyToManyField(to='Equipment.ItemTypeSpec')),
            ],
        ),
    ]
