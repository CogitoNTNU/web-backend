from django.test import TestCase, client

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
        self.assertEqual(response.status_code, 400)
