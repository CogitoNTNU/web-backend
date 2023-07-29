from django.db import models

class Member(models.Model):
    order = models.IntegerField('Order', primary_key=True, max_length=2, blank=True, default=0)
    name = models.CharField('Name', max_length=30, blank=True, default='')
    title = models.CharField('Title', max_length=30, blank=True, default='')
    image = models.ImageField('Image', null=True, blank=True, upload_to="images/")
    category = models.CharField('Category', max_length=30, blank=True, default='')
    email = models.EmailField('Email', max_length=50, blank=True, default='')
    linkedIn = models.URLField('LinkedIn', max_length=200, blank=True, default='')

    def __str__(self) -> str:
        return self.name
