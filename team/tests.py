from django.test import TestCase, client

from team.models import Member, ProjectDescription

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

        self.assertEqual(response.status_code, 400)

    def test_invalid_missing_first_name_payload(self):
        data = {
            "first_name": "",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_missing_last_name_payload(self):
        data = {
            "first_name": "John",
            "last_name": "",
            "email": "user@domain.com",
            "phone_number": "1234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_missing_phone_number_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_invalid_to_short_phone_number_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "123",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_international_phone_numbers(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "+491234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)


class GetProjectsDescriptionsTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.url = f"{base}projects-description/"
        # Create some Member and ProjectDescription objects for testing
        member1 = Member.objects.create(
            name="Jane Doe", email="jane@example.com", order=2
        )
        member2 = Member.objects.create(
            name="John Doe", email="john@example.com", order=1
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
        project2.leaders.add(member2)

    def tearDown(self) -> None:
        # Clean up run after every test method.
        ProjectDescription.objects.all().delete()
        Member.objects.all().delete()

    def test_get_all_projects(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Project 1", response.content.decode())
        self.assertIn("Project 2", response.content.decode())

    def test_get_leader_from_project(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Jane Doe", response.content.decode())
        self.assertIn("John Doe", response.content.decode())
