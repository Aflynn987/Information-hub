# Generated by Django 4.2.1 on 2023-05-12 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info_hubs', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='info_hubs.category'),
        ),
    ]
