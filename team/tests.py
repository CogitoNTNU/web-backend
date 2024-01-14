from django.test import TestCase, Client
from team.models import Member, MemberApplication
from rest_framework import status

# Create your tests here.

base = "/api/"


class GetMembersTestCase(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.client = Client()
        self.url = f"{base}members-by-type/"  # Assuming this is your endpoint for get_members view

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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Alice", response.content.decode())

    def test_get_members_by_category(self):
        response = self.client.post(self.url, {"member_type": "Another Category"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Bob", response.content.decode())
        self.assertNotIn("Alice", response.content.decode())

    def test_get_members_invalid_category(self):
        response = self.client.post(self.url, {"member_type": "Invalid Category"})

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

    def test_short_phone_number_payload(self):
        payload = self.valid_payload.copy()
        payload["phone_number"] = "123"

        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the amount of applications in the database has increased by 1
        self.assertEqual(
            MemberApplication.objects.count(),
            self.amount_of_applications_before_test + 1,
        )

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
