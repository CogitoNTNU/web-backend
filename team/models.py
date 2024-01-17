from django.db import models

# Create your models here.


class Member(models.Model):
    order = models.IntegerField(
        "Order", primary_key=True, blank=True, default=0, help_text=" The order of the member in the list to be displayed on the frontend")
    name = models.CharField("Name", max_length=30, blank=True,
                            default="", help_text=" The full name of the member")
    title = models.CharField("Title", max_length=30, blank=True, default="",
                             help_text=" The title of the member, like 'CEO' or 'Team Lead'")
    image = models.ImageField("Image", null=True, blank=True,
                              upload_to="images/", help_text=" The image of the member")
    category = models.CharField("Category", max_length=30, blank=True, default="",
                                help_text=" The category of the member, like 'Styret' or 'Web', different from title like 'CEO'")
    email = models.EmailField("Email", max_length=50, blank=True,
                              unique=False, default="", help_text=" The email of the member")
    github = models.URLField("GitHub", max_length=200, blank=True,
                             default="", help_text=" The link of the member's GitHub profile")
    linkedIn = models.URLField(
        "LinkedIn", max_length=200, blank=True, default="", help_text="The link of the member's LinkedIn profile")

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
    about = models.TextField(
        blank=True, help_text="Applicant's main application")
    date_of_application = models.DateTimeField(
        auto_now_add=True,  # Use auto_now_add for the creation timestamp
        help_text="The date and time the application was sent",
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ProjectDescription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    # Add leader members using ManyToManyField, referencing 'email' field of Member
    leaders = models.ManyToManyField(Member)
    hours_a_week = models.IntegerField()

    def __str__(self) -> str:
        return self.name
