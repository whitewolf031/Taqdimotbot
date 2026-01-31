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