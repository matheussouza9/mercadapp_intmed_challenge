# Generated by Django 2.0 on 2017-12-12 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_cart_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date',
            new_name='payment_date',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_appointment',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='carts', to='core.Market'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='carts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='core.Cart'),
        ),
    ]
