from django.test import TestCase, Client
from team.models import Member, MemberApplication

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

    def test_apply_invalid_email(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = "invalid-email"

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_invalid_missing_email_payload(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["email"] = ""

        response = self.client.post(self.url, invalid_payload, format="json")
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
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
        self.assertEqual(response.status_code, 400)
        # Check that the error message contains the field name
        self.assertIn("phone_number", response.data)

        # Check that the application was not created in the database
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test,
        )

    def test_apply_successful(self):
        response = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(response.status_code, 200)
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

    def test_short_phone_number_payload(self):
        payload = self.valid_payload.copy()
        payload["phone_number"] = "123"

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_international_phone_numbers(self):
        payload = self.valid_payload.copy()
        payload["phone_number"] = "+491234567890"

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_long_about_section_payload(self):
        payload = self.valid_payload.copy()
        payload["about"] = "Lorem ipsum" * 1000

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

    def test_valid_empty_about_section_payload(self):
        payload = self.valid_payload.copy()
        payload["about"] = ""

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )
