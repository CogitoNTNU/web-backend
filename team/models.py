from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class MemberCategory(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Member(models.Model):
    order = models.IntegerField(
        "Order",
        primary_key=True,
        blank=True,
        default=0,
        help_text=" The order of the member in the list to be displayed on the frontend",
    )
    name = models.CharField(
        "Name",
        max_length=30,
        blank=True,
        default="",
        help_text=" The full name of the member",
    )
    title = models.CharField(
        "Title",
        max_length=30,
        blank=True,
        default="",
        help_text=" The title of the member, like 'CEO' or 'Team Lead'",
    )
    image = models.ImageField(
        "Image",
        null=True,
        blank=True,
        upload_to="images/",
        help_text=" The image of the member",
    )

    category = models.ManyToManyField(MemberCategory)

    email = models.EmailField(
        "Email",
        max_length=50,
        blank=True,
        unique=False,
        default="",
        help_text=" The email of the member",
    )
    github = models.URLField(
        "GitHub",
        max_length=200,
        blank=True,
        default="",
        help_text=" The link of the member's GitHub profile",
    )
    linkedIn = models.URLField(
        "LinkedIn",
        max_length=200,
        blank=True,
        default="",
        help_text="The link of the member's LinkedIn profile",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return self.name


class MemberApplication(models.Model):
    first_name = models.CharField(max_length=100, help_text="Applicant's first name")
    last_name = models.CharField(max_length=100, help_text="Applicant's last name")
    email = models.EmailField(help_text="Applicant's email address")
    phone_number = models.CharField(max_length=15, help_text="Applicant's phone number")
    about = models.TextField(blank=True, help_text="Applicant's main application")
    date_of_application = models.DateTimeField(
        auto_now_add=True,  # Use auto_now_add for the creation timestamp
        help_text="The date and time the application was sent",
    )
    projects_to_join = models.JSONField(
        default=list,
        blank=True,
        help_text="List of projects the applicant wants to join, in order of preference",
    )
    lead = models.BooleanField(
        default=False,
        blank=True,
        null=True,
        help_text="Whether the applicant wants to be a project lead",
    )
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Semester(models.TextChoices):
    SPRING = "SP", "Spring"
    FALL = "FA", "Fall"


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo = models.ImageField(upload_to="images/")
    # Add leader members using ManyToManyField, referencing 'email' field of Member
    hours_a_week = models.IntegerField()
    github_link = models.URLField(
        max_length=200,
        blank=True,
        default="https://github.com/CogitoNTNU",
        help_text="The link to the project's GitHub repository",
    )

    members = models.ManyToManyField(
        Member,
        through="ProjectMember",
        related_name="projects",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProjectMember(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="project_memberships",
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="roles",
    )

    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(2000)],
        default=timezone.now().year,
    )
    semester = models.CharField(
        max_length=2,
        choices=Semester.choices,
        default=Semester.FALL,
    )

    role = models.CharField(max_length=50)

    class Meta:
        unique_together = (
            "member",
            "project",
            "year",
            "semester",
        )
        ordering = ["-year", "-semester", "project__name"]

    def __str__(self):
        return (
            f"{self.member.name} - {self.project.name} "
            f"({self.get_semester_display()} {self.year})"
        )
