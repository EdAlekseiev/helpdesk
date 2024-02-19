from django.test import TestCase
from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework.test import APIClient

from helpdesk_requests.models import Request
from users.models import User
from users.utils import constants


class RequestViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)
        self.client_group = Group.objects.get(name=constants.CLIENT_GROUP_NAME)
        self.client_user = User.objects.create(username="client_user", password="password", phone="0682389705")
        self.client_user2 = User.objects.create(username="client_user2", password="password", phone="0682389706")
        self.client_user.groups.add(self.client_group)
        self.client_user2.groups.add(self.client_group)
        self.operator_user = User.objects.create(username="operator_user", password="password")
        self.operator_user.groups.add(self.operator_group)
        self.request_data = {
            "body": "Test Request Body",
        }
        self.request1 = Request.objects.create(body="Request 1", initiator=self.client_user)
        self.request2 = Request.objects.create(body="Request 2", initiator=self.client_user2)

    def test_create_client_request(self):
        # Ensure a client can create a request for themselves
        self.client.force_authenticate(user=self.client_user)
        response = self.client.post(reverse("helpdesk_requests:request-clients-list"), self.request_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Request.objects.count(), 3)

    def test_create_operator_request(self):
        # Ensure an operator can't create a request
        self.client.force_authenticate(user=self.operator_user)
        response = self.client.post(reverse("helpdesk_requests:request-operators-list"), self.request_data)
        self.assertEqual(response.status_code, 403)

    def test_access_client_requests(self):
        # Ensure only authenticated clients can access their requests
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 401)

    def test_access_operator_requests(self):
        # Ensure only authenticated operators can access all requests
        self.client.force_authenticate(user=self.operator_user)
        response = self.client.get(reverse("helpdesk_requests:request-operators-list"))
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("helpdesk_requests:request-operators-list"))
        self.assertEqual(response.status_code, 401)

    def test_access_own_requests(self):
        # Ensure a client can access only their own requests
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["body"], self.request1.body)

        self.client.force_authenticate(user=self.client_user2)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["body"], self.request2.body)

    def test_access_other_client_requests(self):
        # Ensure a client cannot access requests of other clients
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["body"], self.request1.body)

        self.client.force_authenticate(user=self.client_user2)
        response = self.client.get(reverse("helpdesk_requests:request-clients-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["body"], self.request2.body)

        # Check if the request of client_user1 is not accessible by client_user2
        self.client.force_authenticate(user=self.client_user2)
        response = self.client.get(
            reverse(
                "helpdesk_requests:request-clients-detail",
                kwargs={"pk": self.request1.pk},
            )
        )
        self.assertEqual(response.status_code, 404)  # Client should not have access to other client's requests
