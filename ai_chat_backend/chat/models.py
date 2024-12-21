from django.db import models

class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"
