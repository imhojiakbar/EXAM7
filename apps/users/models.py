from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.shared.models import AbstractModel
from apps.users.utils import avatar_path


# Create your models here.

class User(AbstractUser, AbstractModel):
    avatar = models.ImageField(upload_to=avatar_path, default="user_avatar.jpg")
