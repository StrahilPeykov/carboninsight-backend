# Generated by Django 5.2 on 2025-06-02 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_company_unique_reference_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productemissionoverridefactor',
            old_name='emission',
            new_name='product',
        ),
    ]
