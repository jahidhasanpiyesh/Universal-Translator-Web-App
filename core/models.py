from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pics/', default='default.png', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='translations')
    source_text = models.TextField()
    translated_text = models.TextField()
    target_lang = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.source_text[:20]}'