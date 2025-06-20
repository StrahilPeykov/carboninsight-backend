# Generated by Django 5.2 on 2025-05-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_emissionoverridefactor_co_2_emission_factor_non_biogenic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emissionoverridefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='emissionoverridefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='materialemissionreferencefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='materialemissionreferencefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productemissionoverridefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productemissionoverridefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productionenergyemissionreferencefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='productionenergyemissionreferencefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='transportemissionreferencefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='transportemissionreferencefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='userenergyemissionreferencefactor',
            name='co_2_emission_factor_biogenic',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='userenergyemissionreferencefactor',
            name='co_2_emission_factor_non_biogenic',
            field=models.FloatField(default=0.0),
        ),
    ]
