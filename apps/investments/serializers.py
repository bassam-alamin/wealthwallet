from rest_framework import serializers
from .models import InvestmentAccount, Transaction, InvestmentAccountMembership


class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class InvestmentAccountMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccountMembership
        fields = '__all__'
