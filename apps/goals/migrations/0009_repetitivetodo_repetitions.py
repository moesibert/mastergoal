# Generated by Django 2.2.4 on 2019-11-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_auto_20191110_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='repetitivetodo',
            name='repetitions',
            field=models.PositiveSmallIntegerField(default=None, null=True),
        ),
    ]