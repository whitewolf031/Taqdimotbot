from django.db import models

class User(models.Model):
    chat_id = models.BigIntegerField(
        unique=True,
        help_text="Telegram chat ID"
    )
    username = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Telegram username"
    )
    first_name = models.CharField(
        max_length=150,
        help_text="Telegram first name"
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Telegram last name"
    )
    is_active = models.BooleanField(
        default=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.chat_id}"

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('payme', 'Payme'),
        ('manual', 'Manual'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Payment amount"
    )
    method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        help_text="Payment method"
    )
    status = models.BooleanField(
        default=False,
        help_text="Payment confirmed"
    )
    receipt_image = models.ImageField(
        upload_to='payments/receipts/',
        null=True,
        blank=True,
        help_text="Receipt image for manual payment"
    )
    verified_by_ai = models.BooleanField(
        default=False,
        help_text="Whether the receipt was verified by AI"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when payment was confirmed"
    )

    class Meta:
        db_table = "payments"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Payment {self.id} - {self.user.chat_id} - {self.amount}"