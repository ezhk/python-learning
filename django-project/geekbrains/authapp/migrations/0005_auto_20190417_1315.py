# Generated by Django 2.2 on 2019-04-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20190414_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(null=True, verbose_name='Возраст'),
        ),
    ]
