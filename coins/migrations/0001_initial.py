# Generated by Django 3.2.10 on 2021-12-29 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('coin_id', models.CharField(blank=True, max_length=200, null=True)),
                ('symbol', models.CharField(max_length=200)),
                ('price', models.FloatField(blank=True, default=0, null=True)),
                ('rank', models.IntegerField(blank=True, default=0, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('market_cap', models.CharField(blank=True, max_length=200, null=True)),
                ('fully_diluted_valuation', models.CharField(blank=True, max_length=200, null=True)),
                ('total_volume', models.CharField(blank=True, max_length=200, null=True)),
                ('highest_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('lowest_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('price_change_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('price_change_percentage_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('market_cap_change_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('market_cap_change_percentage_in_the_last_24h', models.FloatField(blank=True, default=0, null=True)),
                ('circulating_supply', models.FloatField(blank=True, default=0, null=True)),
                ('total_supply', models.FloatField(blank=True, default=0, null=True)),
                ('max_supply', models.FloatField(blank=True, default=0, null=True)),
                ('all_time_high', models.FloatField(blank=True, default=0, null=True)),
                ('all_time_high_change_percentage', models.FloatField(blank=True, default=0, null=True)),
                ('all_time_high_date', models.DateTimeField(blank=True, null=True)),
                ('all_time_low', models.FloatField(blank=True, default=0, null=True)),
                ('all_time_low_change_percentage', models.FloatField(blank=True, default=0, null=True)),
                ('all_time_low_date', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('price_change_in_the_last_1hr', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
    ]