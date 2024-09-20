import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.investments.models import Transaction, InvestmentAccount, PermissionEnums


User = get_user_model()


class AdminTransactionViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            first_name='admin', last_name="admin", email='admin@test.com', password='admin123', is_staff=True,
            is_admin=True
        )
        self.user = User.objects.create_user(
            first_name='user', last_name="last_name", email='bassam+1@gmail.com', password='bassam1234'
        )

        self.account_1 = InvestmentAccount.objects.create(
            name="Investment Account 1",
            description="The user should only have view rights and should not be able to make transactions."
        )
        self.transaction_1 = Transaction.objects.create(
            user=self.user,
            amount=500,
            currency="USD",
            transaction_reference=f"{uuid.uuid4()}",
            transaction_type="deposit",
            status="successful",
            account=self.account_1,
        )
        self.transaction_2 = Transaction.objects.create(
            user=self.user,
            amount=200,
            currency="USD",
            transaction_reference=f"{uuid.uuid4()}",
            transaction_type="withdrawal",
            status="successful",
            account=self.account_1
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_retrieve_user_transactions_success(self):
        url = reverse('admin-view-transactions', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertIn('total_balance', response.data)
        self.assertEqual(len(response.data['transactions']), 2)
        self.assertEqual(response.data['total_balance'], 300)

    def test_admin_retrieve_user_transactions_with_date_filter(self):
        url = reverse('admin-view-transactions', kwargs={'user_id': self.user.id})
        response = self.client.get(f"{url}?start_date=2024-09-01&end_date=2024-09-30")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 2)

    def test_admin_retrieve_user_transactions_no_transactions(self):
        new_user = User.objects.create_user(
            first_name='new_user', last_name="last_name", email='new_user@gmail.com', password='newpass1234'
        )
        url = reverse('admin-view-transactions', kwargs={'user_id': new_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('transactions', response.data)
        self.assertEqual(len(response.data['transactions']), 0)
        self.assertEqual(response.data['total_balance'], 0.0)

    def test_admin_retrieve_user_transactions_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('admin-view-transactions', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AddUserToAccountViewTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            first_name='admin', last_name="admin", email='admin@test.com', password='admin123', is_staff=True,
            is_admin=True
        )
        self.user = User.objects.create_user(
            first_name='user', last_name="last_name", email='bassam+1@gmail.com', password='bassam1234'
        )
        self.account = InvestmentAccount.objects.create(
            name="Investment Account",
            description="Test Account"
        )
        self.client.force_authenticate(user=self.admin_user)

    def test_add_user_to_account_success(self):
        url = reverse('add-user-to-account')
        data = {
            "user": self.user.id,
            "account": self.account.id,
            "permission": PermissionEnums.VIEWER.value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user'], self.user.id)
        self.assertEqual(response.data['account'], self.account.id)

    def test_add_user_to_account_invalid_data(self):
        url = reverse('add-user-to-account')
        data = {
            "user": "invalid_user_id",
            "account": self.account.id,
            "permission": PermissionEnums.VIEWER.value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_add_user_to_account_missing_field(self):
        url = reverse('add-user-to-account')
        data = {
            "user": self.user.id,
            "permission": PermissionEnums.VIEWER.value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_add_user_to_account_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('add-user-to-account')
        data = {
            "user": self.user.id,
            "account": self.account.id,
            "permission": PermissionEnums.VIEWER.value
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
