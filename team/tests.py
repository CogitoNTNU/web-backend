from io import BytesIO
import json
import tempfile
from PIL import Image

from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status

from team.models import Member, MemberApplication, MemberCategory, ProjectDescription

# Create your tests here.
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


def _create_temp_image():
    image = Image.new("RGB", (100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix=".jpg")
    image.save(temp_file, "JPEG")
    temp_file.seek(0)
    return temp_file


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

    def test_update_member_images_success(self):
        temp_image1 = _create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        temp_image2 = _create_temp_image()
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
        temp_image1 = _create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        temp_image2 = _create_temp_image()
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
        temp_image1 = _create_temp_image()
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
        temp_image2 = _create_temp_image()
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
        temp_image1 = _create_temp_image()
        temp_image1.name = self.member1.name + ".jpg"

        response = self.client.post(
            self.url, {"images": [temp_image1]}, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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


class ProjectTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = f"{base}projects/"

        self.member1 = Member.objects.create(
            name="John_Doe", order=1, email="johndoe@cogito-ntnu.no", title="CEO"
        )
        self.member2 = Member.objects.create(
            name="Jane_Smith", order=2, email="janesmith@cogito-ntnu.no", title="CTO"
        )

        self.existing_project_1 = ProjectDescription.objects.create(
            name="Project 1",
            description="This is a project",
            image="image.jpg",
        )
        self.existing_project_1.leaders.add(self.member1)
        self.existing_project_1.leaders.add(self.member2)
        self.existing_project_1.save()

        self.existing_project_2 = ProjectDescription.objects.create(
            name="Project 2",
            description="This is another project",
            image="image2.jpg",
        )
        self.existing_project_2.leaders.add(self.member1)
        self.existing_project_2.save()

    def test_get_all_projects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.existing_project_1.name, response.content.decode())
        self.assertIn(self.existing_project_2.name, response.content.decode())

    def test_unauthorized_add_project(self):
        payload = {
            "name": "New Project",
            "description": "This is a new project",
            "image": _create_temp_image(),
            "leaders": [self.member1.email],
            "hours_a_week": 4,
        }

        response = self.client.post(self.url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_add_project(self):
        # Authenticate the user
        User.objects.create_user(username="testuser", password="testpass")
        login_success = self.client.login(username="testuser", password="testpass")
        self.assertTrue(login_success)

        payload = {
            "name": "New Project",
            "description": "This is a new project",
            "image": _create_temp_image(),
            "leaders": [self.member1.email],
            "hours_a_week": 4,
        }

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            ProjectDescription.objects.filter(name=payload["name"]).exists()
        )
