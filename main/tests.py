import uuid
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main import models, views


class StaticTestCase(TestCase):
    def test_index_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_coc_get(self):
        response = self.client.get(reverse("coc"))
        self.assertEqual(response.status_code, 200)


class SubscriptionTestCase(TestCase):
    def test_index_post(self):
        response = self.client.post(
            reverse("index"),
            {
                "email": "tester@example.com",
            },
        )

        # verify request
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thanks! Email saved—we’ll be in touch soon!")

        # verify model
        self.assertEqual(models.Subscription.objects.all().count(), 1)
        self.assertEqual(
            models.Subscription.objects.all()[0].email, "tester@example.com"
        )

        # verify email message
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("New subscription: tester@example.com", mail.outbox[0].subject)
        self.assertIn("tester@example.com", mail.outbox[0].body)

        # verify email headers
        self.assertEqual(mail.outbox[0].to, [settings.ADMINS[0][1]])
        self.assertEqual(
            mail.outbox[0].from_email,
            settings.SERVER_EMAIL,
        )


class UnsubscribeTestCase(TestCase):
    def setUp(self):
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )

    def test_unsubscribe_get(self):
        response = self.client.get(
            reverse("unsubscribe_key", args=(self.subscription.unsubscribe_key,)),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tester@example.com deleted from mailing list.")
        self.assertFalse(
            models.Subscription.objects.filter(id=self.subscription.id).exists()
        )


class UnsubscribeInvalidTestCase(TestCase):
    def setUp(self):
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )

    def test_unsubscribe_invalid_get(self):
        random_uuid = str(uuid.uuid4())
        response = self.client.get(
            reverse("unsubscribe_key", args=(random_uuid,)),
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid link")
        self.assertTrue(
            models.Subscription.objects.filter(id=self.subscription.id).exists()
        )


class EventTestCase(TestCase):
    def setUp(self):
        self.event = models.Event.objects.create(
            slug="meetup-1",
            title="Sci-Hub Meetup",
            scheduled_at=timezone.now(),
            location="Newspeak House",
            gmaps_url="https://g.co/",
        )

    def test_event_get_404(self):
        response = self.client.get(reverse("event", args=("non-existent-event",)))
        self.assertEqual(response.status_code, 404)

    def test_event_get(self):
        response = self.client.get(reverse("event", args=(self.event.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_event_ics_get(self):
        response = self.client.get(reverse("event_ics", args=(self.event.slug,)))
        self.assertEqual(response.status_code, 200)


class AnnounceTestCase(TestCase):
    def setUp(self):
        self.event = models.Event.objects.create(
            slug="meetup-1",
            title="Sci-Hub Meetup",
            scheduled_at=timezone.now(),
            location="Newspeak House",
            gmaps_url="https://g.co/",
        )
        self.subscription = models.Subscription.objects.create(
            email="tester@example.com"
        )
        self.user = auth_models.User.objects.create(username="alice")
        self.client.force_login(self.user)

    def test_announce_get(self):
        response = self.client.get(
            reverse("dashboard_announce"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Announce Meetup")

    def test_announce_invalid_dryrun_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("dashboard_announce"),
                {
                    "subject": "Meetup Announcement",
                    "body": "Hey! We're having a meetup :D",
                    "dryrun": True,
                },
            )
            self.assertEqual(response.status_code, 200)
            self.assertContains(
                response, "Dry run email for campaign preview does not exist."
            )

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 0)

            # verify email message
            self.assertEqual(len(mail.outbox), 0)

    def test_announce_post(self):
        with patch.object(
            # Django default test runner overrides SMTP EmailBackend with locmem,
            # but because we re-import the SMTP backend in
            # views.mail.get_connection, we need to mock it here too.
            views.mail,
            "get_connection",
            return_value=mail.get_connection(
                "django.core.mail.backends.locmem.EmailBackend"
            ),
        ):
            response = self.client.post(
                reverse("dashboard_announce"),
                {
                    "subject": "Meetup Announcement",
                    "body": "Hey! We're having a meetup :D",
                    "dryrun": False,
                },
                follow=True,
            )

            # verify request
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "1 emails sent.")

            # verify model
            self.assertEqual(models.EmailRecord.objects.all().count(), 1)
            self.assertEqual(
                models.EmailRecord.objects.all()[0].email,
                "tester@example.com",
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subject,
                "Meetup Announcement",
            )
            self.assertIn(
                "Hey! We're having a meetup :D",
                models.EmailRecord.objects.all()[0].body,
            )
            self.assertEqual(
                models.EmailRecord.objects.all()[0].subscription,
                self.subscription,
            )
            self.assertNotEqual(
                models.EmailRecord.objects.all()[0].sent_at,
                None,
            )

            # verify email message
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn("Meetup Announcement", mail.outbox[0].subject)
            self.assertIn("Hey! We're having a meetup :D", mail.outbox[0].body)

            # verify email headers
            self.assertEqual(mail.outbox[0].to, ["tester@example.com"])
            self.assertEqual(
                mail.outbox[0].from_email,
                settings.DEFAULT_FROM_EMAIL,
            )
