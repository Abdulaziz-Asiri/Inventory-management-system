from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/defaultAvatar.png")


    def __str__(self) -> str:
        return self.user.username

