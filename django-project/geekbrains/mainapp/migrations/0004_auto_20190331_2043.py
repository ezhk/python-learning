# Generated by Django 2.1.7 on 2019-03-31 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190330_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAndProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Products')),
            ],
            options={
                'verbose_name': 'Link between products and properties',
                'verbose_name_plural': 'Links between products and properties',
            },
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='property')),
            ],
            options={
                'verbose_name': 'Product property',
                'verbose_name_plural': 'Product properties',
            },
        ),
        migrations.RemoveField(
            model_name='productproperty',
            name='product',
        ),
        migrations.DeleteModel(
            name='ProductProperty',
        ),
        migrations.AddField(
            model_name='productandproperty',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Properties'),
        ),
    ]