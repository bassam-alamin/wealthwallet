from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import InvestmentAccountViewSet, TransactionViewSet


urlpatterns = [
    path('accounts', InvestmentAccountViewSet.as_view(
        {
            "post": "create"
        }
    ), name='investment-account-create'),
    path('accounts/<id>', InvestmentAccountViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "partial_destroy"
        }
    ), name='investment-account-cms'),
    path('transactions', TransactionViewSet.as_view(
        {
            "post": "create"
        }
    ), name='transactions-create'),
    path('transactions/<id>', TransactionViewSet.as_view(
        {
            "get": "retrieve"
        }
    ), name='transactions-retrieve')
]
