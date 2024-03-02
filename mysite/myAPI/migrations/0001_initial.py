# Generated by Django 5.0.2 on 2024-03-01 19:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, unique=True)),
                ('start_date_time', models.CharField(default='2024-03-01 22:50', max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('min_stud_in_group', models.IntegerField(default=1)),
                ('max_stud_in_group', models.IntegerField(default=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]