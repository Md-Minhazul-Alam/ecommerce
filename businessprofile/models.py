from django.db import models

# Create your models here.
class WebsiteSetting(models.Model):
    website_name = models.CharField(max_length=100, default='')
    website_tagline = models.CharField(max_length=100, default="")
    website_description = models.TextField(default='')
    website_logo= models.ImageField(upload_to='website/', null=True, blank=True)
    website_favicon = models.ImageField(upload_to='website/', null=True, blank=True)
    website_thumbnail = models.ImageField(upload_to='website/', null=True, blank=True)
    website_address = models.CharField(max_length=255, default='www.')
    website_contact_phone = models.CharField(max_length=15, default='')
    website_contact_email = models.EmailField(default='')
    website_office_hour = models.TextField(default='Mon-Fri : 10:00 AM - 5:00 PM', null=True, blank=True)

    def __str__(self):
        return self.website_name