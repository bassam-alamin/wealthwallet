from rest_framework.permissions import BasePermission
from apps.investments.models import InvestmentAccountMembership, PermissionEnums
from utils.data_filter import get_or_none


class AccountPermissions(BasePermission):

    def has_permission(self, request, view):
        account = view.kwargs.get('pk')
        if not account:
            return False

        membership = get_or_none(
            InvestmentAccountMembership,
            account_id=account, user=request.user
        )

        if request.method == 'GET' and membership.permission in [PermissionEnums.ADMIN, PermissionEnums.VIEWER]:
            return True
        elif request.method in ['POST', 'PUT', 'DELETE'] and membership.permission == PermissionEnums.ADMIN:
            return True
        elif request.method == 'POST' and membership.permission == PermissionEnums.POSTER:
            return True

        return False

