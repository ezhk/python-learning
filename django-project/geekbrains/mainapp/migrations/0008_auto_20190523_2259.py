# Generated by Django 2.2 on 2019-05-23 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20190417_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True, verbose_name='active'),
        ),
    ]
