# Generated by Django 3.1.3 on 2020-11-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_web', '0004_auto_20201126_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='VisitorsCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
            ],
        ),
    ]
