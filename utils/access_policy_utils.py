from rest_access_policy import AccessPolicy
from apps.investments.models import InvestmentAccountMembership, PermissionEnums, Transaction
from utils.data_filter import get_or_none


# Noqa

class InvestmentAccountAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["retrieve"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["is_viewer"]
        },
        {
            "action": ["create"],
            "principal": ["*"],  # Anyone can create an account
            "effect": "allow"
        },
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["is_account_admin"]
        }
    ]

    def is_viewer(self, request, view, action):
        account_id = view.kwargs.get('id')
        print(account_id)
        membership = get_or_none(
            InvestmentAccountMembership,
            user=request.user, account_id=account_id)
        if not membership:
            return False
        return membership and membership.permission in [PermissionEnums.VIEWER , PermissionEnums.ADMIN]

    def is_account_admin(self, request, view, action):
        account_id = view.kwargs.get('id')
        membership = InvestmentAccountMembership.objects.filter(
            user=request.user, account_id=account_id
        ).first()
        return membership and membership.permission == PermissionEnums.ADMIN


class TransactionAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["retrieve"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["transaction_view_only"]
        },
        {
            "action": ["create"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["transaction_post_only"]
        },
        {
            "action": ["update", "partial_update", "destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["is_account_admin"]
        }
    ]

    def transaction_view_only(self, request, view, action):
        """Check if the user has viewing permission for the transaction's account"""
        transaction_id = view.kwargs.get('id')
        transaction = get_or_none(
            Transaction,id=transaction_id
        )
        if not transaction:
            return False
        account = transaction.account
        membership = get_or_none(
            InvestmentAccountMembership,
            user=request.user, account=account
        )
        if not membership:
            return False
        return membership and membership.permission in [PermissionEnums.VIEWER, PermissionEnums.ADMIN]

    def transaction_post_only(self, request, view, action):
        """Check if the user has permission to post transactions for the account"""
        account = request.data.get("account")
        membership = get_or_none(InvestmentAccountMembership,user=request.user, account_id=account)
        if not membership:
            return False
        return membership and membership.permission in [PermissionEnums.POSTER, PermissionEnums.ADMIN]

    def is_account_admin(self, request, view, action):
        """Check if the user has admin permission for the transaction's account"""
        transaction = view.get_object()
        account = transaction.account
        membership = get_or_none(InvestmentAccountMembership,user=request.user, account_id=account)
        if not membership:
            return False
        return membership and membership.permission == PermissionEnums.ADMIN
