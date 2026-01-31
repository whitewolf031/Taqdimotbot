from payments.models import Payment

def has_active_payment(user) -> bool:
    """
    User da tasdiqlangan payment bormi?
    """
    return Payment.objects.filter(
        user=user,
        status=True
    ).exists()
