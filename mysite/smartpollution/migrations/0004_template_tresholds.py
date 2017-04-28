# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 13:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartpollution', '0003_auto_20170424_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartpollution.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Tresholds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_trigger', models.DecimalField(decimal_places=10, max_digits=19)),
                ('upper_trigger', models.DecimalField(decimal_places=10, max_digits=19)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartpollution.Device')),
                ('metric_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartpollution.Metric')),
            ],
        ),
    ]
