import logging
from django.contrib.auth import get_user_model
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_access_policy import AccessViewSetMixin

from utils.access_policy_utils import InvestmentAccountAccessPolicy, TransactionAccessPolicy
from utils.data_filter import get_or_none
from .models import InvestmentAccount, Transaction
from .serializers import InvestmentAccountSerializer, TransactionSerializer

User = get_user_model()

logging = logging.getLogger('investment_views')



class InvestmentAccountViewSet(AccessViewSetMixin, viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer
    access_policy = InvestmentAccountAccessPolicy
    lookup_field = 'id'

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def retrieve(self, request, id=None):
        try:
            account = get_or_none(InvestmentAccount, id=id)
            serializer = self.serializer_class(account)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem retrieving account details",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem creating account",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, id=None):
        try:
            account = get_or_none(InvestmentAccount, id=id)
            serializer = self.serializer_class(account, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem updating account",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_update(self, request, id=None):
        try:
            account = get_or_none(InvestmentAccount, id=id)
            serializer = self.serializer_class(account, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem updating account",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def partial_destroy(self, request, id=None):
        try:
            account = get_or_none(InvestmentAccount, id=id)
            if account is None:
                raise APIException('Account not found')
            account.is_deleted = True
            account.save()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem updating account",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TransactionViewSet(AccessViewSetMixin, viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    access_policy = TransactionAccessPolicy
    lookup_field = 'id'

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def retrieve(self, request, id=None):
        try:
            transaction = get_or_none(Transaction, id=id)
            serializer = self.serializer_class(transaction)
            return Response(
                serializer.data
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem retrieving transactions",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem Creating transactions",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )



