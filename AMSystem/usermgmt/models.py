from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    birthdate = models.DateField()
    password = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)

    class Meta:
        unique_together = ('first_name', 'last_name') 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"