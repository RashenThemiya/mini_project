# home/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from market_place.models import Profile  # ✅ Import Profile

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def clean(self):
        """Ensure only sellers can create posts."""
        if not hasattr(self.author, 'profile') or self.author.profile.user_type != 'seller':
            raise ValidationError("Only sellers can create posts.")

    def save(self, *args, **kwargs):
        """Validate before saving."""
        self.clean()
        super().save(*args, **kwargs)
