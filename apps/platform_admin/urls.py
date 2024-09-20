from django.urls import path
from apps.platform_admin.views import AddUserToAccountView, AdminTransactionViewSet

urlpatterns = [
    path('accounts/add-user',
         AddUserToAccountView.as_view(), name='add-user-to-account'),
    path('transactions/<user_id>', AdminTransactionViewSet.as_view(
        {
            "get": "retrieve"
        }
    ), name='admin-view-transactions'),
]