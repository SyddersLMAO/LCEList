from django.contrib.auth.models import AbstractUser
from django.db import models
from content.validators import validate_image_size
from content.utils import crop_to_square

class User(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='images/profile_photo.png', validators=[validate_image_size],)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.username = self.username.lower() if not self.pk else self.username
        if self.avatar and hasattr(self.avatar, 'file'):
            self.avatar = crop_to_square(self.avatar)
        super().save(*args, **kwargs)