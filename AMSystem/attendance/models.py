from django.db import models
from django.conf import settings

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"