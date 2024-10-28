from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
from django.db import models

class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, first_name, last_name, department, email, birthdate, contact_number, password=None):
        if not employee_id:
            raise ValueError("The employee ID is required.")
        if not email:
            raise ValueError("An email address is required.")
        
        email = self.normalize_email(email)
        employee_group, _ = Group.objects.get_or_create(name='Employee')
        
        employee = self.model(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            department=department,
            email=email,
            birthdate=birthdate,
            contact_number=contact_number,
            group=employee_group,
        )
        employee.set_password(password or '123456')  # Set default password if none provided
        employee.save(using=self._db)
        return employee

    def create_superuser(self, employee_id, first_name, last_name, department, email, birthdate, contact_number, password=None):
        employee = self.create_user(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            department=department,
            email=email,
            birthdate=birthdate,
            contact_number=contact_number,
            password=password,
        )
        employee.is_staff = True
        employee.is_superuser = True
        employee.role = 'admin'  # Set the role to admin
        
        employee.save(using=self._db)  # Save before assigning to the group
        
        admin_group, _ = Group.objects.get_or_create(name='Administrator')
        employee.group = admin_group
        employee.save(using=self._db)  # Save again after group assignment

        return employee

class Employee(AbstractBaseUser, PermissionsMixin):
    employee_id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=100, unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=[('employee', 'Employee'), ('admin', 'Administrator')], default='employee')

    group = models.ForeignKey(
        Group,
        related_name="employees",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    objects = EmployeeManager()

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department', 'email', 'birthdate']

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.employee_id})"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
