from io import BytesIO
from django.test import TestCase, Client
from PIL import Image
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from team.models import Member, ProjectDescription
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

base = "/api/"


class MemberTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.url = f"{base}apply/"
        self.valid_payload = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
        }

    def tearDown(self) -> None:
        # Clean up run after every test method.
        pass

    def test_invalid_missing_email_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "+491234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetProjectsDescriptionsTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.url = f"{base}projects-description/"
        # Create some Member and ProjectDescription objects for testing
        member1 = Member.objects.create(
            name="Jane Doe", email="jane@example.com", order=1
        )
        member2 = Member.objects.create(
            name="John Doe", email="john@example.com", order=2
        )

        project1 = ProjectDescription.objects.create(
            name="Project 1",
            description="Description for Project 1",
            hours_a_week=10,
        )
        project1.leaders.add(member1)

        project2 = ProjectDescription.objects.create(
            name="Project 2",
            description="Description for Project 2",
            hours_a_week=20,
        )
        project2.leaders.add(member1)
        project2.leaders.add(member2)

    def tearDown(self) -> None:
        # Clean up run after every test method.
        ProjectDescription.objects.all().delete()
        Member.objects.all().delete()

    def test_get_all_projects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Project 1", response.content.decode())
        self.assertIn("Project 2", response.content.decode())

    def test_get_leader_from_project(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Jane Doe", response.content.decode())
        self.assertIn("John Doe", response.content.decode())

    def test_project_details(self):
        response = self.client.get(self.url)
        data = response.json()

        # Check the details of the first project
        self.assertEqual(data[0]["name"], "Project 1")
        self.assertEqual(data[0]["description"], "Description for Project 1")
        self.assertEqual(data[0]["hours_a_week"], 10)
        self.assertEqual(len(data[0]["leaders"]), 1)
        self.assertEqual(data[0]["leaders"][0]["name"], "Jane Doe")

    def test_project_details_with_several_leaders(self):
        response = self.client.get(self.url)
        data = response.json()

        # Check the details of the Second project
        self.assertEqual(data[1]["name"], "Project 2")
        self.assertEqual(data[1]["description"], "Description for Project 2")
        self.assertEqual(data[1]["hours_a_week"], 20)
        self.assertEqual(len(data[1]["leaders"]), 2)
        self.assertEqual(data[1]["leaders"][0]["name"], "Jane Doe")
        self.assertEqual(data[1]["leaders"][1]["name"], "John Doe")


class AddProjectDescriptionTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = APIClient()
        self.url = f"{base}add-project-description/"

        # The endpoint requires authentication, so we need to create a user
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)

        self.member1 = Member.objects.create(
            name="Alice",
            title="CEO",
            email="alice@example.com",
            order=1,
            # Add other fields as necessary
        )
        self.member2 = Member.objects.create(
            name="Bob",
            title="Teamlead",
            email="bob@example.com",
            order=2,
        )

        # Need to create a dummy image
        image = Image.new("RGB", (100, 100), color="red")
        image_file = BytesIO()
        image.save(image_file, format="JPEG")
        image_file.name = "test_image.jpg"
        image_file.seek(0)
        # Project data
        self.valid_project_data = {
            "name": "Test Project",
            "description": "A test project description",
            "image": SimpleUploadedFile(
                name="test_image.jpg",
                content=image_file.read(),
                content_type="image/jpeg",
            ),
            "leaders": [self.member1.email],
            "hours_a_week": 10,
        }

        self.invalid_project_data = {
            # Missing 'name' and other required fields
            "description": "Incomplete project description",
        }

        self.invalid_project_data_missing_name = {
            "name": "",
            "description": "Description of new project",
            "hours_a_week": 15,
        }
        self.invalid_project_data_missing_image = {
            "name": "New Project",
            "description": "Description of new project",
            "hours_a_week": 15,
            "image": None,
        }

    def tearDown(self) -> None:
        # Clean up run after every test method.
        ProjectDescription.objects.all().delete()
        User.objects.all().delete()

    def test_add_project_description_success(self):
        response = self.client.post(
            self.url, self.valid_project_data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_status.HTTP_200_OK_OK)
        self.assertEqual(ProjectDescription.objects.count(), 1)

    def test_add_project_description_success_with_several_leaders(self):
        # Add a second member as a leader

        project_data = self.valid_project_data.copy()
        project_data["leaders"].append(self.member2.email)

        response = self.client.post(self.url, project_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_status.HTTP_200_OK_OK)
        self.assertEqual(ProjectDescription.objects.count(), 1)
        # Check that the project has three leaders
        project = ProjectDescription.objects.first()
        self.assertEqual(project.leaders.count(), 2)

    def test_add_project_invalid_data_name(self):
        response = self.client.post(
            self.url, self.invalid_project_data_missing_name, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_status.HTTP_400_BAD_REQUEST_BAD_REQUEST
        )
        self.assertEqual(ProjectDescription.objects.count(), 0)

    def test_add_project_invalid_image(self):
        response = self.client.post(
            self.url, self.invalid_project_data_missing_image, format="json"
        )

        self.assertEqual(
            response.status_code, status.HTTP_status.HTTP_400_BAD_REQUEST_BAD_REQUEST
        )
        self.assertEqual(ProjectDescription.objects.count(), 0)

    def test_add_project_invalid_data_field_validation(self):
        # Create project data with an invalid 'hours_a_week' field
        invalid_data = self.valid_project_data.copy()
        invalid_data["hours_a_week"] = "invalid"

        response = self.client.post(self.url, invalid_data, format="multipart")

        self.assertEqual(
            response.status_code, status.HTTP_status.HTTP_400_BAD_REQUEST_BAD_REQUEST
        )
        self.assertEqual(ProjectDescription.objects.count(), 0)

    def test_add_project_description_unauthenticated(self):
        # Log out the current user
        self.client.logout()

        response = self.client.post(
            self.url, self.valid_project_data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(ProjectDescription.objects.count(), 0)

    def test_add_project_invalid_leaders(self):
        # Create project data with invalid leader identifiers
        invalid_leaders_data = self.valid_project_data.copy()
        invalid_leaders_data["leaders"] = [
            "nonexistent@example.com",
            "invalid@example.com",
        ]

        response = self.client.post(self.url, invalid_leaders_data, format="multipart")

        self.assertEqual(
            response.status_code, status.HTTP_status.HTTP_400_BAD_REQUEST_BAD_REQUEST
        )

        # Check that no new project description is added to the database
        self.assertEqual(ProjectDescription.objects.count(), 0)
