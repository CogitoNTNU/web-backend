from django.db import models

# Create your models here.

class ProjectDescription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    leader = models.CharField(max_length=100)
    hours_a_week = models.IntegerField()


    def __str__(self) -> str:
        return self.name

class Member(models.Model):
    order = models.IntegerField(
        "Order", primary_key=True, blank=True, default=0)
    name = models.CharField("Name", max_length=30, blank=True, default="")
    title = models.CharField("Title", max_length=30, blank=True, default="")
    image = models.ImageField(
        "Image", null=True, blank=True, upload_to="images/")
    category = models.CharField(
        "Category", max_length=30, blank=True, default="")
    email = models.EmailField("Email", max_length=50, blank=True, default="")

    github = models.URLField("GitHub", max_length=200, blank=True, default="")
    linkedIn = models.URLField(
        "LinkedIn", max_length=200, blank=True, default="")

    def __str__(self) -> str:
        return self.name


class MemberApplication(models.Model):
    first_name = models.CharField(
        max_length=100, help_text="Applicant's first name")
    last_name = models.CharField(
        max_length=100, help_text="Applicant's last name")
    email = models.EmailField(help_text="Applicant's email address")
    phone_number = models.CharField(
        max_length=15, help_text="Applicant's phone number")
    about = models.CharField(
        max_length=300, blank=True, help_text="Applicant's main application")
    date_of_application = models.DateTimeField(
        auto_now_add=True,  # Use auto_now_add for the creation timestamp
        help_text="The date and time the application was sent",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
