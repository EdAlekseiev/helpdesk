from django.conf import settings
from django.db import models


class RequestStatusChoices(models.TextChoices):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"


class Request(models.Model):
    body = models.TextField()
    status = models.CharField(
        max_length=16,
        choices=RequestStatusChoices.choices,
        default=RequestStatusChoices.PENDING,
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tickets",
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="processed_tickets",
    )

