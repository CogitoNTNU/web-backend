from django.db import models

# Create your models here.


class Image(models.Model):
    image_url = models.CharField(max_length=1000, blank=True, default="", help_text=" The image url")
    prompt = models.CharField(max_length=1000, blank=True, default="", help_text=" The prompt used to generate the image")
    date_of_generation = models.DateTimeField(auto_now_add=True, help_text="The date and time the image was generated")
    height = models.IntegerField(blank=True, default=0, help_text="The height of the image")
    width = models.IntegerField(blank=True, default=0, help_text="The width of the image")

    def __str__(self) -> str:
        return self.image_url
    