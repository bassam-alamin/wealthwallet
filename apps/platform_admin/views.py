import logging
from django.db.models import Sum, Case, When, F
from django.utils.dateparse import parse_date
from knox.auth import TokenAuthentication
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.investments.models import Transaction
from apps.investments.serializers import (TransactionSerializer,
                                          InvestmentAccountMembershipSerializer)

logging = logging.getLogger('platform_admin_views')


class AdminTransactionViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser, ]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def retrieve(self, request, user_id=None, *args, **kwargs):
        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')

            if start_date:
                start_date = parse_date(start_date)
            if end_date:
                end_date = parse_date(end_date)

            transactions = Transaction.objects.filter(
                user_id=user_id,
                is_deleted=False
            )
            if start_date and end_date:
                transactions = transactions.filter(created_at__range=[start_date, end_date])
            elif start_date:
                transactions = transactions.filter(created_at__gte=start_date)
            elif end_date:
                transactions = transactions.filter(created_at__lte=end_date)

            total_balance = transactions.aggregate(
                total_balance=Sum(
                    Case(
                        When(transaction_type="deposit", status="successful", then=F('amount')),
                        When(transaction_type="withdrawal", status="successful", then=-F('amount')),
                        default=0.0
                    )
                )
            )['total_balance'] or 0.0
            serializer = self.serializer_class(transactions, many=True)
            return Response({
                "transactions": serializer.data,
                "total_balance": total_balance
            })
        except Exception as error:
            logging.error(error)
            return Response(
                {
                    "message": "Problem retrieving transactions",
                    "detail": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class AddUserToAccountView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_serializer(self, *args, **kwargs):
        return InvestmentAccountMembershipSerializer(*args, **kwargs)

    def post(self, request):
        try:
            serializer = self.get_serializer(
                data=request.data
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logging.error(e)
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
