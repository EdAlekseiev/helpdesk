from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from rest_framework.test import APIClient

from users.models import User
from users.utils import constants


class PublicClientViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_group = Group.objects.get(name=constants.CLIENT_GROUP_NAME)
        self.client_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890",
        }

    def test_create_client(self):
        # Ensure a client can be created
        response = self.client.post(reverse("users:clients-list"), self.client_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        created_user = User.objects.first()
        self.assertEqual(created_user.first_name, self.client_data["first_name"])
        self.assertEqual(created_user.last_name, self.client_data["last_name"])
        self.assertEqual(created_user.phone, self.client_data["phone"])
        self.assertEqual(created_user.username, self.client_data["phone"])  # Username should be phone number
        self.assertTrue(created_user.is_client)

    def test_client_serializer_generate_password(self):
        # Ensure client serializer generates a temporary password
        response = self.client.post(reverse("users:clients-list"), self.client_data)
        self.assertEqual(response.status_code, 201)
        created_user = User.objects.first()
        self.assertTrue(created_user.password)

    def test_client_permissions(self):
        # Ensure only clients have access to their own data
        non_client = User.objects.create(username="nonclient", phone="+9999999999")
        self.client.force_authenticate(user=non_client)
        response = self.client.get(reverse("users:clients-list"))
        self.assertEqual(response.status_code, 403)  # Non-client should not have access


class PrivateClientViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.client_group = Group.objects.get(name=constants.CLIENT_GROUP_NAME)
        self.client_user = User.objects.create(username="client", phone="+1234567890")
        self.client_user.groups.add(self.client_group)
        self.client.force_authenticate(user=self.client_user)

    def test_client_permissions(self):
        # Ensure only clients have access to their own data
        response = self.client.get(reverse("users:clients-list"))
        self.assertEqual(response.status_code, 200)
