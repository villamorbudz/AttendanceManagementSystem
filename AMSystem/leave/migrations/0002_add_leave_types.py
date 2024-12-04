from django.db import migrations


def add_leave_types(apps, schema_editor):
    LeaveType = apps.get_model('leave', 'LeaveType')
    leave_types = [
        'Vacation Leave',
        'Sick Leave',
        'Casual Leave',
        'Maternity/Paternity Leave',
        'Bereavement Leave',
        'Unpaid Leave',
        'Other'
    ]
    for leave_name in leave_types:
        LeaveType.objects.create(name=leave_name)

class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_leave_types),
    ]
