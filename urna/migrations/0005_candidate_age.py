# Generated by Django 4.1.1 on 2022-09-13 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urna', '0004_ndturn_stturn_delete_turns'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='age',
            field=models.IntegerField(default=0),
        ),
    ]
