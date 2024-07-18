from django.db import models
from django.utils import timezone
from django.conf import settings

class Post(models.Model):
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    content = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=(
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('deleted', 'Deleted'),
        ),
        default='draft'
    )

    def __str__(self):
        return self.title
