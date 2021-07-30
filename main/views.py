from django import forms
from django.contrib import messages
from django.core.mail import mail_admins
from django.shortcuts import render

from main import models


def index(request):
    if request.method == "GET":
        return render(request, "main/index.html")

    elif request.method == "POST":

        class SubscriptionForm(forms.ModelForm):
            class Meta:
                model = models.Subscription
                fields = ["email"]

        form = SubscriptionForm(request.POST)
        form.save()

        submitter_email = form.cleaned_data["email"]
        mail_admins(
            f"New subscription: {submitter_email}",
            f"Someone new has subscribed to Sci-Hub London. Hooray!\n\nIt's {submitter_email}\n",
        )

        messages.success(request, "Thanks! Email saved—we’ll be in touch soon!")
        return render(request, "main/index.html")
