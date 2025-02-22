from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Helper function to define the file path for uploaded sticker images
def sticker_image_path(instance, filename):
    return f'stickers/{filename}'

# Define WARD_CHOICES globally so both models can use it
WARD_CHOICES = [
    ('Gintota', 'Gintota'),
    ('Dadalla', 'Dadalla'),
    ('Bope', 'Bope'),
    ('Kumbalwella', 'Kumbalwella'),
    ('Madawalamulla', 'Madawalamulla'),
    ('Deddugoda', 'Deddugoda'),
    ('Maitipe', 'Maitipe'),
    ('Dangedara', 'Dangedara'),
    ('Bataganvila', 'Bataganvila'),
    ('Sangamiththapura', 'Sangamiththapura'),
    ('Galwadugoda', 'Galwadugoda'),
    ('Kandewaththa', 'Kandewaththa'),
    ('Kaluwella', 'Kaluwella'),
    ('Galle Town', 'Galle Town'),
    ('Weliwaththa', 'Weliwaththa'),
    ('Thalapitiya', 'Thalapitiya'),
    ('Makuluwa', 'Makuluwa'),
    ('Milidduwa', 'Milidduwa'),
    ('Magalle', 'Magalle'),
    ('Katugoda', 'Katugoda'),
]

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

    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    report_id = models.CharField(max_length=50, unique=True, blank=True)
    image = models.ImageField(upload_to=sticker_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Public Safety Incidents')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Low')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    ward = models.CharField(max_length=50, choices=WARD_CHOICES, default='Galle Town') 
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.report_id:
            self.report_id = f'STKR-{int(now().timestamp())}'
        super(Sticker, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.report_id} - {self.category} - {self.ward} - {self.priority}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['report_id'], name='unique_sticker_report_id')
        ]

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ward = models.CharField(max_length=100, choices=WARD_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.ward}"
