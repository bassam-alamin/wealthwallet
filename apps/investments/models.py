import enum
from django.contrib.auth import get_user_model
from django.db import models

from apps.auth_app.models import BaseModel

User = get_user_model()


class TransactionStatuses(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESSFUL = "successful"
    CANCELLED = "cancelled"
    FAILED = "failed"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class TransactionTypeEnums(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PermissionEnums(str, enum.Enum):
    VIEWER = "viewer"  # Can only view
    POSTER = "poster"  # Can only post transactions
    ADMIN = "admin"  # Full CRUD permissions

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

# Create your models here.
class InvestmentAccount(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    available_amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    @property
    def members(self):
        """ Return all users (members) for this account """
        return User.objects.filter(investmentaccountmembership__account=self)


class InvestmentAccountMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey("InvestmentAccount", on_delete=models.CASCADE, related_name="memberships")
    permission = models.CharField(max_length=10, choices=PermissionEnums.choices(), default=PermissionEnums.VIEWER)

    def __str__(self):
        return f"{self.user.first_name} - {self.permission} for {self.account.name}"

    class Meta:
        unique_together = ["user", "account"]


class Transaction(BaseModel):
    amount = models.FloatField(default=0.0)
    currency = models.CharField(default="KES")
    transaction_reference = models.UUIDField()
    transaction_type = models.CharField(
        choices=TransactionTypeEnums.choices(),
        max_length=255
    )
    status = models.CharField(choices=TransactionStatuses.choices(), max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} - {self.transaction_reference}"
