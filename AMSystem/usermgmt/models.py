from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Role Model
class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Ensure name is unique
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def create_role(cls, name, is_staff=False):
        role, created = cls.objects.get_or_create(name=name, defaults={'is_staff': is_staff})
        if created:
            print(f"Role '{name}' created.")
        else:
            print(f"Role '{name}' already exists.")
        return role

# Department Model
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Ensure name is unique

    def __str__(self):
        return self.name

    @classmethod
    def create_department(cls, name):
        department, created = cls.objects.get_or_create(name=name)
        if created:
            print(f"Department '{name}' created.")
        else:
            print(f"Department '{name}' already exists.")
        return department

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **extra_fields):
        if not user_id:
            raise ValueError('The User ID must be set')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Role.objects.get(name="Administrator"))
        extra_fields.setdefault('department', Department.objects.get(name="Dev Team"))

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(user_id, password, **extra_fields)

# Custom User Model
class User(AbstractUser):
    username = None  # Remove default username field
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=50, unique=True)  # Custom user ID
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthdate = models.DateField()
    contact_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Profile image field
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    objects = UserManager()  # Attach the custom user manager

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'birthdate', 'contact_number', 'email']

    def save(self, *args, **kwargs):
        if self.role:
            self.is_staff = self.role.is_staff  # Set is_staff based on role
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Account Model (optional, depending on your requirements)
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    password = models.CharField(max_length=255)  # You might want to hash the password or store it securely

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

