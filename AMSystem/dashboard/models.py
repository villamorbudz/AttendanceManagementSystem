# Create your models here.
# from django.db import models
# # from django.contrib.auth.models import User
# from django.conf import settings
# from django.contrib.auth.models import User

from django.db import models
from django.conf import settings

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.status}"


class LeaveBalance(models.Model):
    employee = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    annual_leave_balance = models.IntegerField(default=20)  # Default annual leave

    def __str__(self):
        return f"{self.employee.username} - {self.annual_leave_balance} days"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default-profile.png')

    def __str__(self):
        return f"{self.user.username}'s Profile"
