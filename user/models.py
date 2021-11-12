from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    staff = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=20,null=True)
    profile_pic = models.ImageField(default='profile_pics/avatar.png',upload_to ='profile_pics')

    def __str__(self) -> str:
        return f'{self.staff}\'s Profile'