from django.db import models

# Home SLider
class HeroSlider(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    subtitle = models.CharField(max_length=200, verbose_name="Subtitle")
    image = models.ImageField(upload_to='hero_sliders/', verbose_name="Image")
    link = models.URLField(max_length=200, blank=True, null=True, verbose_name="Link")

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
        return self.title 