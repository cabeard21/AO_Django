# Generated by Django 3.1.7 on 2021-11-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Equipment', '0006_auto_20210218_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market', models.CharField(max_length=50)),
            ],
        ),
    ]
