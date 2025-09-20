from django.db import models
from django.utils.text import slugify

# Tag Model
class Tag(models.Model):
    tag = models.CharField(max_length=100, default='')
    tag_slug = models.SlugField(max_length=100, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        # If slug is empty, generate from tag
        if not self.tag_slug:
            base_slug = slugify(self.tag)
        else:
            base_slug = slugify(self.tag_slug)

        # Uniqueness
        slug = base_slug
        num = 1
        while Tag.objects.filter(tag_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        self.tag_slug = slug
        super().save(*args, **kwargs)

# Brand Model
class Brand(models.Model):
    brand = models.CharField(max_length=100, default='')
    brand_slug = models.SlugField(max_length=100, unique=True, blank=True)
    brand_image = models.ImageField(upload_to='brand_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand

    def save(self, *args, **kwargs):
        # If brand_slug is empty, generate from brand
        if not self.brand_slug:
            base_slug = slugify(self.brand)
        else:
            base_slug = slugify(self.brand_slug)

        # Uniqueness
        slug = base_slug
        num = 1
        while Brand.objects.filter(brand_slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        self.brand_slug = slug
        super().save(*args, **kwargs)


