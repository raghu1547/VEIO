# Generated by Django 3.0.7 on 2020-06-29 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vn', models.CharField(max_length=20, verbose_name='Vehicle Number')),
                ('timein', models.DateTimeField(auto_now_add=True)),
                ('timeout', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Gesveh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vn', models.CharField(max_length=20, verbose_name='Vehicle Number')),
                ('name', models.CharField(max_length=20, verbose_name='Entrant Name')),
                ('contact', models.CharField(max_length=20, verbose_name='Entrant Contact')),
                ('nod', models.IntegerField(default=1, verbose_name='Permission Time')),
                ('firstentry', models.DateTimeField(auto_now_add=True, verbose_name='First Entry time')),
            ],
            options={
                'verbose_name': 'Guest Vehicle',
                'verbose_name_plural': 'Guest Vehicles',
            },
        ),
        migrations.CreateModel(
            name='Regveh',
            fields=[
                ('vn', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Vehicle Number')),
                ('name', models.CharField(max_length=20, verbose_name='Owner Name')),
                ('post', models.CharField(max_length=20)),
                ('contact', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Registered Vehicle',
                'verbose_name_plural': 'Registered Vehicles',
            },
        ),
    ]
