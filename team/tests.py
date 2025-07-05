import os
import json
import tempfile
from PIL import Image

from django.core import mail
from django.core.files.storage import default_storage
from django.core.management import call_command, CommandError
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status


from team.models import (
    Member,
    MemberApplication,
    MemberCategory,
    Project,
    ProjectMember,
    Semester,
)


base = "/api/"


class GetMembersTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        # Assuming this is your endpoint for get_members view
        self.url = f"{base}members-by-type/"

        # Create some MemberCategory objects for testing
        styret_category = MemberCategory.objects.create(title="Styret")
        another_category = MemberCategory.objects.create(title="Another Category")

        # Create some Member objects for testing
        alice = Member.objects.create(
            name="Alice",
            order=1,
            email="Alice@domain.com",
            title="CEO",
        )
        alice.category.set([styret_category])

        bob = Member.objects.create(
            name="Bob",
            order=2,
            email="Bob@domain.com",
            title="CTO",
        )
        bob.category.set([another_category])

    def tearDown(self) -> None:
        # Clean up run after every test method.
        Member.objects.all().delete()

    def test_get_all_members(self):
        response = self.client.get(self.url, {"member_type": "Alle Medlemmer"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Alice", response.content.decode())

    def test_get_members_by_category(self):
        response = self.client.get(self.url, {"member_type": "Another Category"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Bob", response.content.decode())
        self.assertNotIn("Alice", response.content.decode())

    def test_get_members_invalid_category(self):
        response = self.client.get(self.url, {"member_type": "Invalid Category"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), "[]")


class MemberWithProjectsTests(TestCase):
    def setUp(self):
        self.url = f"{base}members-by-type/"

        self.cat_dev = MemberCategory.objects.create(title="Developer")
        self.cat_ops = MemberCategory.objects.create(title="Operations")

        self.alice = Member.objects.create(
            order=1,
            name="Alice",
            title="Backend Dev",
            email="alice@example.com",
        )

        self.bob = Member.objects.create(
            order=2,
            name="Bob",
            title="SysAdmin",
            email="bob@example.com",
        )

        self.charlie = Member.objects.create(
            order=3,
            name="Charlie",
            title="Frontend Dev",
            email="charlie@example.com",
        )

        # Create two projects
        self.proj_web = Project.objects.create(
            name="Web Development",
            description="Build web application",
            hours_a_week=10,
        )
        self.proj_game_ai = Project.objects.create(
            name="Game AI",
            description="Develop AI for games",
            hours_a_week=8,
        )

        # Assign Alice to both projects, Bob to one and Charlie to none
        ProjectMember.objects.create(
            member=self.alice,
            project=self.proj_web,
            role="Backend Developer",
            year=2021,
            semester=Semester.SPRING,
        )
        ProjectMember.objects.create(
            member=self.alice,
            project=self.proj_web,
            role="Frontend Developer",
            year=2021,
            semester=Semester.FALL,
        )
        ProjectMember.objects.create(
            member=self.alice,
            project=self.proj_game_ai,
            role="Contributor",
            year=2021,
            semester=Semester.FALL,
        )
        ProjectMember.objects.create(
            member=self.bob,
            project=self.proj_game_ai,
            role="Support",
            year=2021,
            semester=Semester.FALL,
        )

    def test_get_all_members_includes_projects(self):
        """
        GET /members/?member_type=Alle Medlemmer
        should return both all members and their project memberships.
        each member with a project should have a `project_memberships` list containing:
          - project name
          - role
          - year
          - semester
        """
        response = self.client.get(self.url, {"member_type": "Alle Medlemmer"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), Member.objects.count())

        # Check Alice's data
        alice_data = next((m for m in data if m["name"] == self.alice.name), None)
        self.assertIn("project_memberships", alice_data)
        self.assertEqual(
            len(alice_data["project_memberships"]),
            self.alice.project_memberships.count(),
        )

        for project_member in alice_data["project_memberships"]:
            self.assertIn("project", project_member)
            self.assertIn("name", project_member["project"])
            self.assertIn("role", project_member)
            self.assertIn("year", project_member)
            self.assertIn("semester", project_member)


class ApplyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f"{base}apply/"

        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "about": "I am a developer, who loves AI",
            "lead": True,
        }
        self.amount_of_applications_before_test = MemberApplication.objects.count()

    def test_sending_of_email(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Application sent in successfully")

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Application Received by Cogito NTNU", mail.outbox[0].subject)
        self.assertIn(f"Dear John Doe,", mail.outbox[0].body)

    def test_apply_invalid_email(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

        # Check that an email was not sent
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_missing_email_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = ""

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_invalid_missing_first_name_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["first_name"] = ""

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the error message contains the field name
        self.assertIn("first_name", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_invalid_missing_last_name_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["last_name"] = ""

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the error message contains the field name
        self.assertIn("last_name", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_invalid_missing_phone_number_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["phone_number"] = ""

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the error message contains the field name
        self.assertIn("phone_number", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_invalid_too_long_names(self):
        payload = self.valid_payload.copy()
        payload["first_name"] = "a" * 101
        payload["last_name"] = "a" * 101
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_apply_successful(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Application sent in successfully", response.data["message"])

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.filter(email="johndoe@example.com").exists()
        )
        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_invalid_missing_first_name_payload(self):
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_missing_last_name_payload(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "user@domain.com",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_missing_phone_number_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_to_short_phone_number_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "123",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_international_phone_numbers(self):
        payload = self.valid_payload.copy()
        payload["phone_number"] = "+491234567890"

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_long_about_section_payload(self):
        payload = self.valid_payload.copy()
        payload["about"] = "Lorem ipsum" * 1000

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_empty_about_section_payload(self):
        payload = self.valid_payload.copy()
        payload["about"] = ""

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_norwegian_names(self):
        payload = self.valid_payload.copy()
        payload["first_name"] = "ÆØÅ"
        payload["last_name"] = "æøå"

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_duplicate_applications(self):
        """
        Applications with the same fields should be allowed as one might accidentally send in the same application twice,
        or send in an application with the same information as a previous one.
        """
        response1 = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Check that the applications was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 2,
        )

    def test_valid_email_with_subdomain(self):
        payload = self.valid_payload.copy()
        payload["email"] = "user@mail.example.com"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_email_with_dots_in_start(self):
        payload = self.valid_payload.copy()
        payload["email"] = "user.lastname@example.com"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_long_email_address(self):
        payload = self.valid_payload.copy()
        payload["email"] = "a" * 100 + "@example.com"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_numeric_email_local_part(self):
        payload = self.valid_payload.copy()
        payload["email"] = "1234567890@example.com"
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_application_with_projects_to_join(self):
        payload = self.valid_payload.copy()
        projects_to_join = ["Project 1", "Project 2", "Project 3"]
        payload["projects_to_join"] = json.dumps(projects_to_join)
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

        # Check that the member has the projects_to_join field set
        application = MemberApplication.objects.get(email=self.valid_payload["email"])
        self.assertEqual(application.projects_to_join, projects_to_join)

    def test_invalid_application_with_projects_to_join(self):
        payload = self.valid_payload.copy()
        projects_to_join = "Project 1, Project 2, Project 3"
        payload["projects_to_join"] = json.dumps(projects_to_join)
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the application was not created in the database
        self.assertTrue(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )


class UpdateMemberImageViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = f"{base}member/image"
        self.authenticated_user = User.objects.create_user(
            username="testuser", password="testpass"
        )

        self.member1 = Member.objects.create(
            name="John_Doe", order=1, email="johndoe@cogito-ntnu.no", title="CEO"
        )
        self.member2 = Member.objects.create(
            name="Jane_Smith", order=2, email="janesmith@cogito-ntnu.no", title="CTO"
        )

    def tearDown(self):
        # Clean up uploaded images after each test
        for member in Member.objects.all():
            if member.image and default_storage.exists(member.image.path):
                default_storage.delete(member.image.path)

    def _create_temp_image(self):
        image = Image.new("RGB", (100, 100))
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
        image.save(temp_file, "JPEG")
        temp_file.seek(0)
        return temp_file

    def test_update_member_images_success(self):
        temp_image1 = self._create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        temp_image2 = self._create_temp_image()
        temp_image2.name = self.member2.name + ".jpg"

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url, {"images": [temp_image1, temp_image2]}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("updated_members", response.data)
        self.assertIn("members_not_found", response.data)
        self.assertEqual(len(response.data["updated_members"]), 2)
        self.assertEqual(len(response.data["members_not_found"]), 0)

    def test_update_member_images_partial_success(self):
        temp_image1 = self._create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        temp_image2 = self._create_temp_image()
        temp_image2.name = "Non_Existent.jpg"

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url, {"images": [temp_image1, temp_image2]}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("updated_members", response.data)
        self.assertIn("members_not_found", response.data)
        self.assertEqual(len(response.data["updated_members"]), 1)
        self.assertEqual(len(response.data["members_not_found"]), 1)

    def test_update_member_who_has_image(self):
        temp_image1 = self._create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            self.url, {"images": [temp_image1]}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("updated_members", response.data)
        self.assertIn("members_not_found", response.data)
        self.assertEqual(len(response.data["updated_members"]), 1)
        self.assertEqual(len(response.data["members_not_found"]), 0)

        # Update the image of the same member
        temp_image2 = self._create_temp_image()
        temp_image2.name = self.member1.name + ".jpg"

        response = self.client.post(
            self.url, {"images": [temp_image2]}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("updated_members", response.data)
        self.assertIn("members_not_found", response.data)
        self.assertEqual(len(response.data["updated_members"]), 1)
        self.assertEqual(len(response.data["members_not_found"]), 0)

    def test_update_member_images_invalid_request(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(self.url, {}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_member_images_unauthenticated(self):
        temp_image1 = self._create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        response = self.client.post(
            self.url, {"images": [temp_image1]}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MemberCategoryViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = f"{base}member/category"
        self.authenticated_user = User.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_get_member_categories(self):
        self.category1 = MemberCategory.objects.create(title="Styret")
        self.category2 = MemberCategory.objects.create(title="Another Category")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ImportDataCommandTest(TestCase):

    def setUp(self):
        # Create a temp file for JSON data
        self.file_path = "test.json"

    def tearDown(self):
        # Clean up by removing the file after each test
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_import_member_categories(self):
        json_data = [{"title": "Management"}, {"title": "Leadership"}]

        # Write the JSON data to a file
        with open(self.file_path, "w") as file:
            json.dump(json_data, file)

        self.assertEqual(MemberCategory.objects.count(), 0)
        # Simulate calling the command
        call_command("data_importer", "import_member_categories", self.file_path)

        # Check the output and model updates
        self.assertEqual(MemberCategory.objects.count(), 2)

    def test_import_members(self):
        json_data = [
            {
                "order": 1,
                "name": "John Doe",
                "title": "CEO",
                "email": "john.doe@example.com",
                "github": "https://github.com/johndoe",
                "linkedIn": "https://www.linkedin.com/in/johndoe",
                "image": "/media/images/john.jpg",
                "category": ["Management", "Leadership"],
            }
        ]

        # Write the JSON data to a file
        with open(self.file_path, "w") as file:
            json.dump(json_data, file)

        self.assertEqual(Member.objects.count(), 0)
        # Simulate calling the command
        call_command("data_importer", "import_members", self.file_path)

        # Check the output and model updates
        self.assertEqual(Member.objects.count(), 1)

    def test_invalid_subcommand(self):
        with self.assertRaises(CommandError):
            call_command("data_importer", "invalid_subcommand", self.file_path)


class SQLInjectionTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f"{base}apply/"

        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "about": "I am a developer, who loves AI",
        }

    def test_sql_injection_in_about_field(self):
        # A harmless SQL injection attempt for testing purposes.
        # This SQL statement is a no-op (no operation), it should not affect the database.
        sql_injection_payload = "'; SELECT 1; --"

        self.valid_payload["about"] = sql_injection_payload

        response = self.client.post(self.url, self.valid_payload, format="json")

        # Expecting a normal response since Django ORM should safely handle the input
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the 'about' field contains the SQL injection code as plain text
        application = MemberApplication.objects.get(email="johndoe@example.com")
        self.assertEqual(application.about, sql_injection_payload)
        # Verifying that the database integrity is maintained
        self.assertTrue(MemberApplication.objects.exists())
