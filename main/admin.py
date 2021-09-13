from django.contrib import admin

from main import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "created_at",
    )

    ordering = ["-id"]


admin.site.register(models.Subscription, SubscriptionAdmin)


class EmailRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subscription",
        "email",
        "subject",
        "sent_at",
    )

    ordering = ["-id"]


admin.site.register(models.EmailRecord, EmailRecordAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "scheduled_at",
        "location",
    )

    ordering = ["-id"]


admin.site.register(models.Event, EventAdmin)
