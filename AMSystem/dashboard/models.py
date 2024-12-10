# from django.db import models
# from django.contrib.auth import get_user_model
# from django.utils import timezone

# User = get_user_model()

# class Attendance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField(default=timezone.now)
#     check_in = models.DateTimeField(null=True, blank=True)
#     check_out = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=20, default='pending')
    
#     class Meta:
#         unique_together = ['user', 'date']
        
#     def __str__(self):
#         return f"{self.user.username} - {self.date}"

# class Leave(models.Model):
#     LEAVE_TYPES = [
#         ('sick', 'Sick Leave'),
#         ('vacation', 'Vacation'),
#         ('personal', 'Personal'),
#         ('other', 'Other'),
#     ]
    
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     reason = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.leave_type} ({self.start_date} to {self.end_date})"
        
#     class Meta:
#         ordering = ['-created_at']
