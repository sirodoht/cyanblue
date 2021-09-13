import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribe_key = models.UUIDField(default=uuid.uuid4, unique=True)

    def get_unsubscribe_url(self):
        path = reverse("unsubscribe_key", args={self.unsubscribe_key})
        return f"//{settings.CANONICAL_HOST}{path}"

    def __str__(self):
        return self.email


class EmailRecord(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now, null=True)

    # email literate field in case subscription foreign key is null
    # which means user has unsubscribed
    email = models.EmailField()

    class Meta:
        ordering = ["-sent_at"]


class Event(models.Model):
    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    scheduled_at = models.DateTimeField()
    gmaps_url = models.URLField()

    def __str__(self):
        return self.slug
