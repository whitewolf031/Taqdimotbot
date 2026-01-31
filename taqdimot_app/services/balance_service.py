from decimal import Decimal
from django.db.models import Sum
from payments.models import Payment, WorkUsage

def get_user_balance(user):
    """
    User balansini hisoblaydi:
    BALANS = jami to‘lov - jami sarf
    """

    total_paid = Payment.objects.filter(
        user=user,
        status=True
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    total_used = WorkUsage.objects.filter(
        user=user
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    return total_paid - total_used
