# Generated by Django 2.0 on 2017-12-12 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20171212_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='market',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to='core.Market'),
            preserve_default=False,
        ),
    ]
