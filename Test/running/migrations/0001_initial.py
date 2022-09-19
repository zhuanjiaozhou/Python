# Generated by Django 4.0.7 on 2022-09-13 08:34

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('areaid', models.AutoField(primary_key=True, serialize=False)),
                ('countryid', models.PositiveIntegerField()),
                ('chn_name', models.CharField(max_length=64)),
                ('eng_name', models.CharField(blank=True, max_length=64, null=True)),
                ('sort', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'area',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('countryid', models.AutoField(primary_key=True, serialize=False)),
                ('chn_name', models.CharField(max_length=64)),
                ('eng_name', models.CharField(blank=True, max_length=64, null=True)),
                ('country_logo', models.CharField(blank=True, max_length=120, null=True)),
                ('sort', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('provinceid', models.AutoField(primary_key=True, serialize=False)),
                ('areaid', models.PositiveIntegerField(blank=True, null=True)),
                ('chn_name', models.CharField(max_length=64)),
                ('eng_name', models.CharField(blank=True, max_length=64, null=True)),
                ('sort', models.PositiveIntegerField()),
                ('countryid', models.ForeignKey(db_column='countryid', null=True, on_delete=django.db.models.deletion.SET_NULL, to='running.country')),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('cityid', models.AutoField(primary_key=True, serialize=False)),
                ('areaid', models.PositiveIntegerField(blank=True, null=True)),
                ('chn_name', models.CharField(max_length=64)),
                ('eng_name', models.CharField(blank=True, max_length=64, null=True)),
                ('sort', models.PositiveIntegerField()),
                ('Provinceid', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='countryid', chained_model_field='countryid', db_column='provinceid', on_delete=django.db.models.deletion.CASCADE, to='running.province')),
                ('countryid', models.ForeignKey(db_column='countryid', null=True, on_delete=django.db.models.deletion.SET_NULL, to='running.country')),
            ],
            options={
                'db_table': 'city',
            },
        ),
    ]