from django.db import models
from django.conf import settings

class LostFound(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    location = models.CharField(max_length=200)
    date = models.DateField()
    image = models.ImageField(upload_to='lost_found/', blank=True, null=True)
    contact_info = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_status_display()}: {self.title}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lost & Found Item'
        verbose_name_plural = 'Lost & Found Items'
