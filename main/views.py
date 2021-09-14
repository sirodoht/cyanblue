from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import mail
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView

from main import forms, models, utils


def index(request):
    if request.method == "GET":
        return render(request, "main/index.html")
    elif request.method == "POST":
        form = forms.SubscriptionForm(request.POST)

        # if not valid
        if not form.is_valid():
            if "email" in form.errors and form.errors["email"] == [
                "Subscription with this Email already exists."
            ]:
                # if case of already subscribed
                messages.info(request, "Email already subscribed :)")
                return render(
                    request,
                    "main/index.html",
                )

            else:
                # all other cases
                messages.error(
                    request,
                    "Well, that didn't work :/",
                )
                return render(
                    request,
                    "main/index.html",
                    {
                        "form": form,
                    },
                )

        # this branch only executes if form is valid
        form.save()
        submitter_email = form.cleaned_data["email"]
        mail_admins(
            f"New subscription: {submitter_email}",
            f"Someone new has subscribed to Sci-Hub London. Hooray!\n\nIt's {submitter_email}\n",
        )

        messages.success(request, "Thanks! Email saved—we’ll be in touch soon!")
        return render(request, "main/index.html")


def event(request, event_slug):
    return render(
        request,
        "main/event.html",
        {
            "event": models.Event.objects.get(slug=event_slug),
        },
    )


def event_ics(request, event_slug):
    event = models.Event.objects.get(slug=event_slug)
    ics_content = utils.get_ics(event)
    response = HttpResponse(ics_content, content_type="application/octet-stream")
    response["Content-Disposition"] = "attachment; filename=scihub-london-event.ics"
    return response


class DashboardAnnounce(LoginRequiredMixin, FormView):
    form_class = forms.AnnounceForm
    template_name = "main/dashboard_announce.html"
    success_url = reverse_lazy("dashboard_announce")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subscriptions_count"] = models.Subscription.objects.all().count()
        context["subscriptions_list"] = models.Subscription.objects.all().order_by(
            "created_at"
        )
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():

            # handle dry run case
            if form.cleaned_data.get("dryrun"):
                mail_admins(
                    form.cleaned_data.get("subject"),
                    form.cleaned_data.get("body"),
                )
                messages.success(request, "Dry run executed")
                return self.form_valid(form)

            # list of messages to sent out
            message_list = []
            record_ids = []

            # TODO: get event from form, stub for now
            event = models.Event.objects.get()

            # get all subscribers
            subscribers = models.Subscription.objects.all()
            for s in subscribers:

                unsubscribe_url = utils.get_protocol() + s.get_unsubscribe_url()
                body_footer = "\n\n"
                body_footer += "---\n"
                body_footer += "Unsubscribe:\n"
                body_footer += unsubscribe_url + "\n"

                # initialise email record
                email_record = models.EmailRecord.objects.create(
                    subscription=s,
                    email=s.email,
                    subject=form.cleaned_data.get("subject"),
                    body=form.cleaned_data.get("body") + body_footer,
                    sent_at=None,
                )
                record_ids.append(email_record.id)

                # create email message
                ics_content = utils.get_ics(event)
                email = mail.EmailMessage(
                    subject=form.cleaned_data.get("subject"),
                    body=form.cleaned_data.get("body") + body_footer,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[s.email],
                    reply_to=[settings.DEFAULT_FROM_EMAIL],
                    headers={
                        "X-PM-Message-Stream": "announcements",
                        "List-Unsubscribe": unsubscribe_url,
                        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
                    },
                    attachments=[
                        (
                            "scihub-london-event.ics",
                            ics_content,
                            "application/octet-stream",
                        )
                    ],
                )
                message_list.append(email)

            # send out emails
            connection = mail.get_connection(
                "django.core.mail.backends.smtp.EmailBackend",
                host=settings.EMAIL_HOST_BROADCASTS,
            )
            connection.send_messages(message_list)
            models.EmailRecord.objects.filter(id__in=record_ids).update(
                sent_at=timezone.now()
            )

            messages.success(request, f"{len(message_list)} emails sent.")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def unsubscribe_key(request, key):
    if models.Subscription.objects.filter(unsubscribe_key=key).exists():
        subscription = models.Subscription.objects.get(unsubscribe_key=key)
        email = subscription.email
        subscription.delete()
        messages.success(request, f"{email} deleted from mailing list.")
    else:
        messages.info(request, "Invalid link.")
    return redirect("index")


def coc(request):
    return render(request, "main/codeofconduct.html")
