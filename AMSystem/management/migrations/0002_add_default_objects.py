from django.db import migrations
from django.contrib.auth.hashers import make_password
from datetime import datetime

def create_default_objects(apps, schema_editor):
    Role = apps.get_model('management', 'Role')
    Department = apps.get_model('management', 'Department')
    User = apps.get_model('management', 'User')

    employee_role = Role.objects.create(
        name='Employee',
        is_staff=False,
        is_superuser=False
    )
    
    manager_role = Role.objects.create(
        name='Manager',
        is_staff=True,
        is_superuser=False
    )
    
    admin_role = Role.objects.create(
        name='Administrator',
        is_staff=True,
        is_superuser=True
    )

    development_team = Department.objects.create(name='Development Team')
    development_team.role.add(admin_role)

    human_resources = Department.objects.create(name='Human Resources')
    human_resources.role.add(manager_role)

    employee_departments = [
        'Information Technology',
        'Customer Support',
        'Sales',
        'Marketing',
        'Product Development',
        'Quality Assurance',
        'Operations',
        'Finance',
        'Training and Implementation'
    ]

    for dept_name in employee_departments:
        dept = Department.objects.create(name=dept_name)
        dept.role.add(employee_role)

    # Create superuser if it doesn't exist
    if not User.objects.filter(user_id='AMS-0000').exists():
        User.objects.create(
            user_id='AMS-0000',
            password=make_password('admin'),
            first_name='System',
            last_name='Admin',
            birthdate=datetime.strptime('2000-01-01', '%Y-%m-%d').date(),
            contact_number='0',
            email='AMS-0000',
            is_staff=True,
            is_superuser=True,
            department=development_team,
            is_active=True
        )

def remove_default_objects(apps, schema_editor):
    Role = apps.get_model('management', 'Role')
    Department = apps.get_model('management', 'Department')
    User = apps.get_model('management', 'User')
    
    User.objects.filter(user_id='AMS-0000').delete()
    Department.objects.all().delete()
    Role.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_default_objects,
        ),
    ]
