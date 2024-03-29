# Generated by Django 3.1.1 on 2021-01-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20201215_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='itrecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100, unique=True)),
                ('item_r1', models.FloatField(max_length=10, null=True)),
                ('item_r2', models.FloatField(max_length=10, null=True)),
                ('item_r3', models.FloatField(max_length=10, null=True)),
                ('item_r4', models.FloatField(max_length=10, null=True)),
                ('item_r5', models.FloatField(max_length=10, null=True)),
                ('item_r6', models.FloatField(max_length=10, null=True)),
                ('item_r7', models.FloatField(max_length=10, null=True)),
                ('item_r8', models.FloatField(max_length=10, null=True)),
                ('item_r9', models.FloatField(max_length=10, null=True)),
                ('item_r10', models.FloatField(max_length=10, null=True)),
            ],
        ),
    ]
