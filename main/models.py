from django.db import models


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Event(models.Model):
    slug = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    location = models.CharField(max_length=300)
    scheduled_at = models.DateTimeField()

    def __str__(self):
        return self.slug
