# Generated by Django 3.1.1 on 2020-11-08 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20201105_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mini_category',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_category', to='board.category'),
        ),
    ]