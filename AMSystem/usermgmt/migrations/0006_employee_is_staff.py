# Generated by Django 5.1.2 on 2024-10-14 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0005_alter_employee_unique_together_employee_last_login_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]