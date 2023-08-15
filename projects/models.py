from django.db import models

# Create your models here.
class newProject(models.Model):
    title = models.CharField(name="title", primary_key=True, max_length=30, default='', blank=True)
    desc = models.CharField(name="desc", max_length=400, default='', blank=True)
    image = models.ImageField('image', null=True, blank=True, upload_to="images/")

    def __str__(self) -> str:
        return self.title