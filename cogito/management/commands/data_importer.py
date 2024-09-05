import json
from django.core.management.base import BaseCommand, CommandError
from team.models import MemberCategory, MemberApplication, ProjectDescription, Member


class Command(BaseCommand):
    help = "Manage different imports"

    def add_arguments(self, parser):
        # Add a subcommand argument
        parser.add_argument(
            "subcommand",
            type=str,
            help="Subcommand to run (import_member_categories, import_member_applications, import_project_descriptions)",
        )
        parser.add_argument("json_file", type=str, help="Path to the JSON file")

    def handle(self, *args, **options):
        subcommand = options["subcommand"]
        json_file = options["json_file"]

        # Call the relevant function based on subcommand
        if subcommand == "import_members":
            self.import_members(json_file)
        elif subcommand == "import_member_categories":
            self.import_member_categories(json_file)
        elif subcommand == "import_member_applications":
            self.import_member_applications(json_file)
        elif subcommand == "import_project_descriptions":
            self.import_project_descriptions(json_file)
        else:
            raise CommandError(f"Unknown subcommand: {subcommand}")

    def import_members(self, json_file: str):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"File {json_file} does not exist.")

        for item in data:
            categories = item.pop("category", [])
            member, created = Member.objects.update_or_create(
                order=item["order"],
                defaults={
                    "name": item["name"],
                    "title": item["title"],
                    "email": item["email"],
                    "github": item["github"],
                    "linkedIn": item["linkedIn"],
                    "image": item["image"],
                },
            )

            # Add categories
            member.category.clear()
            for (
                category_title
            ) in categories:  # Use 'category_title' since the field is 'title'
                category, _ = MemberCategory.objects.get_or_create(title=category_title)
                member.category.add(category)
                self.stdout.write(self.style.SUCCESS(f"Processed member {member.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported members from {json_file}")
        )

    def import_member_categories(self, json_file: str):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"File {json_file} does not exist.")

        for item in data:
            category, created = MemberCategory.objects.get_or_create(
                title=item["title"]
            )
            self.stdout.write(
                self.style.SUCCESS(f"Processed category {category.title}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported categories from {json_file}")
        )

    def import_member_applications(self, json_file: str):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"File {json_file} does not exist.")

        for item in data:
            application, created = MemberApplication.objects.get_or_create(
                first_name=item["first_name"],
                last_name=item["last_name"],
                defaults={
                    "email": item["email"],
                    "phone_number": item["phone_number"],
                    "about": item["about"],
                    "projects_to_join": item["projects_to_join"],
                },
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Processed application for {application.first_name} {application.last_name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported applications from {json_file}")
        )

    def import_project_descriptions(self, json_file: str):
        try:
            with open(json_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            raise CommandError(f"File {json_file} does not exist.")

        for item in data:
            project, created = ProjectDescription.objects.update_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "hours_a_week": item["hours_a_week"],
                    "image": item["image"],
                },
            )

            # Add leaders (ManyToManyField)
            project.leaders.clear()
            for leader_email in item["leaders"]:
                try:
                    leader = Member.objects.get(email=leader_email)
                    project.leaders.add(leader)
                except Member.DoesNotExist:
                    self.stderr.write(
                        f"Leader with email {leader_email} does not exist."
                    )

            self.stdout.write(self.style.SUCCESS(f"Processed project {project.name}"))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported projects from {json_file}")
        )
