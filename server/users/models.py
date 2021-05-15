from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    email = models.EmailField() # Override email field for set it required
