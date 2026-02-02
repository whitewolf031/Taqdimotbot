from django.db import models
from taqdimot_app.models import User

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=10)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending"
    )

    receipt_file_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    verified_by_ai = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "payments"
        ordering = ["-confirmed_at"]

    def __str__(self):
        return f"Payment {self.id} - {self.user.chat_id} - {self.amount}"

class WorkUsage(models.Model):
    WORK_TYPE_CHOICES = [
        ("referat", "Referat"),
        ("mustaqil", "Mustaqil ish"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="usages"
    )

    work_type = models.CharField(
        max_length=20,
        choices=WORK_TYPE_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="How much balance was used"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "work_usages"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.chat_id} - {self.amount}"