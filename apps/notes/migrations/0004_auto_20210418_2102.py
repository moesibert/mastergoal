# Generated by Django 2.2.16 on 2021-04-18 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20210418_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['updated']},
        ),
    ]