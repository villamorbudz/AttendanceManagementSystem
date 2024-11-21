from django.db import models
from django.conf import settings

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # e.g., 'Present', 'Absent'

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"