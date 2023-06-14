from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='Phone Number')
    address = models.TextField(null=True, blank=True, default='', verbose_name='Address')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username