# Generated by Django 2.0 on 2017-12-10 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('price', models.FloatField()),
                ('amount_available', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Cart')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Market',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('total', models.FloatField(default=0)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Cart')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Market'),
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, through='core.ItemCart', to='core.Item'),
        ),
        migrations.AddField(
            model_name='cart',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Market'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
