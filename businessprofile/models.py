from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField

# Website Setting
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
    

# Quick Link Model
class QuickLink(models.Model):
    title = models.CharField(max_length=200, default='')
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, default='')
    description = HTMLField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If slug is empty, generate from title
        if not self.slug:
            base_slug = slugify(self.title)
        else:
            base_slug = slugify(self.slug)

        # Ensure uniqueness
        slug = base_slug
        num = 1
        while QuickLink.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        self.slug = slug
        super().save(*args, **kwargs)


# Legal Link Model
class LegalLink(models.Model):
    title = models.CharField(max_length=200, default='')
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True, default='')
    description = HTMLField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If slug is empty, generate from title
        if not self.slug:
            base_slug = slugify(self.title)
        else:
            base_slug = slugify(self.slug)

        # Ensure uniqueness
        slug = base_slug
        num = 1
        while LegalLink.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        self.slug = slug
        super().save(*args, **kwargs)