from django.db import models
from usermgmt.models import User

# Create your models here.

class LeaveType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class LeaveRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.ForeignKey(LeaveType, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    status = models.CharField(max_length=50)
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)