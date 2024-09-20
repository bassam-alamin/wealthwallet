import random
import uuid

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken

from apps.investments.models import InvestmentAccount, InvestmentAccountMembership, PermissionEnums

User = get_user_model()


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            first_name='admin', last_name="last_name", email='admin@test.com', password='admin123', is_staff=True,
            is_admin=True
        )
        self.user = User.objects.create_user(
            first_name='user', last_name="last_name", email='bassam+1@gmail.com', password='bassam1234'
        )

        self.account_1 = InvestmentAccount.objects.create(
            name="Investment Account 1",
            description="The user should only have view rights and should not be able to make transactions."
        )
        self.account_2 = InvestmentAccount.objects.create(
            name="Investment Account 2",
            description="The user should have full CRUD (Create, Read, Update, Delete) permissions."
        )
        self.account_3 = InvestmentAccount.objects.create(
            name="Investment Account 3",
            description="The user should only be able to post transactions, but not view them."
        )
        self.view_only = InvestmentAccountMembership.objects.create(
            user=self.user,
            account=self.account_1,
            permission=PermissionEnums.VIEWER
        )
        self.account_admin_user = InvestmentAccountMembership.objects.create(
            user=self.user,
            account=self.account_2,
            permission=PermissionEnums.ADMIN
        )
        self.transaction_poster = InvestmentAccountMembership.objects.create(
            user=self.user,
            account=self.account_3,
            permission=PermissionEnums.POSTER
        )
        self.token = AuthToken.objects.create(
            user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token[1]))

    def test_account_1_view_only_success(self):
        url = reverse('investment-account-cms', kwargs={'id': self.account_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)

    def test_account_1_post_deny(self):
        url = reverse('transactions-create')
        data = {
            "amount": random.randint(100, 1000),
            "currency": "USD",
            "transaction_reference": f"{uuid.uuid4()}",
            "transaction_type": "deposit",
            "status": "successful",
            "account": f"{self.account_1.id}"
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_account_3_post_transaction_only_success(self):
        url = reverse('transactions-create')
        data = {
            "amount": random.randint(100, 1000),
            "currency": "USD",
            "transaction_reference": f"{uuid.uuid4()}",
            "transaction_type": "deposit",
            "status": "successful",
            "account": f"{self.account_3.id}"
        }
        response = self.client.post(path=url, data=data)
        cache.set("transaction_id", response.json().get("id"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)

    def test_account_3_view_deny(self):
        url = reverse('transactions-retrieve',kwargs={"id": cache.get("transaction_id")} )
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
