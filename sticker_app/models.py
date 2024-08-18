from django.db import models

def sticker_image_path(instance, filename):
    return f'stickers/{filename}'

class Sticker(models.Model):
    CATEGORY_CHOICES = [
        ('Public Safety Incidents', 'Public Safety Incidents'),
        ('Public Health and Sanitation', 'Public Health and Sanitation'),
        ('Infrastructure Issues', 'Infrastructure Issues'),
        ('Environmental Concerns', 'Environmental Concerns'),
        ('Social Services and Welfare', 'Social Services and Welfare'),
        ('Community Engagement', 'Community Engagement'),
        ('Emergency Services', 'Emergency Services'),
    ]

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]

    image = models.ImageField(upload_to='stickers/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Public Safety Incidents')
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')

    def __str__(self):
        return f"{self.category} - {self.priority}"
