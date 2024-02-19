from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group

from rest_framework.test import APIClient

from users.models import User
from users.utils import constants


class PublicOperatorViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)
        self.operator_data = {
            "username": "operator1",
            "password": "operator_password",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_create_operator(self):
        # Ensure an operator can be created by anyone
        response = self.client.post(reverse("users:operators-list"), self.operator_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)
        created_user = User.objects.first()
        self.assertEqual(created_user.username, self.operator_data["username"])
        self.assertTrue(created_user.is_operator)

    def test_unique_username(self):
        # Ensure that usernames generated by the serializer are unique
        operator_data1 = {
            "username": "operator2",
            "password": "operator_password",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response1 = self.client.post(reverse("users:operators-list"), operator_data1)
        self.assertEqual(response1.status_code, 201)

        operator_data2 = {
            "username": "operator2",  # Same username as the previous one
            "password": "operator_password",
            "first_name": "Alex",
            "last_name": "Smith",
        }
        response2 = self.client.post(reverse("users:operators-list"), operator_data2)
        self.assertEqual(response2.status_code, 400)  # Duplicate username should return 400 error code

    def test_operator_permissions(self):
        # Ensure only clients have access to their own data
        non_client = User.objects.create(username="nonclient", phone="+9999999999")
        self.client.force_authenticate(user=non_client)
        response = self.client.get(reverse("users:operators-list"))
        self.assertEqual(response.status_code, 403)  # Non-operator should not have access


class PrivateOperatorViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)
        self.operator = User.objects.create(username="client", phone="+1234567890")
        self.operator.groups.add(self.operator_group)
        self.client.force_authenticate(user=self.operator)

    def test_operator_permissions(self):
        # Ensure only operator have access to their own data
        response = self.client.get(reverse("users:operators-list"))
        self.assertEqual(response.status_code, 200)