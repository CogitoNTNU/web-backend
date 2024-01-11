from django.test import TestCase, Client
from team.models import Member

# Create your tests here.

base = "/api/"


class GetMembersTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.url = f"{base}members_by_type/"  # Assuming this is your endpoint for get_members view

        # Create some Member objects for testing

        Member.objects.create(
            category="Styre", name="Alice", order=1, email="Alice@domain.com"
        )
        Member.objects.create(
            category="Another Category", name="Bob", order=2, email="Bob@domain.com"
        )

    def tearDown(self) -> None:
        # Clean up run after every test method.
        Member.objects.all().delete()

    def test_get_all_members(self):
        response = self.client.post(self.url, {"member_type": "Alle Medlemmer"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Alice", response.content.decode())

    def test_get_members_by_category(self):
        response = self.client.post(self.url, {"member_type": "Another Category"})

        self.assertEqual(response.status_code, 200)
        self.assertIn("Bob", response.content.decode())
        self.assertNotIn("Alice", response.content.decode())

    def test_get_members_invalid_category(self):
        response = self.client.post(self.url, {"member_type": "Invalid Category"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "[]")


class MemberApplicationTestCase(TestCase):
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

    def test_valid_long_about_section_payload(self):
        about_section: str = "Lorem ipsum" * 1000
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "1234567890",
            "about": about_section,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

    def test_valid_empty_about_section_payload(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "user@domain.com",
            "phone_number": "1234567890",
            "about": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
