from django import forms

from main import models


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = models.Subscription
        fields = ["email"]


class BroadcastForm(forms.Form):
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    dryrun = forms.BooleanField(
        required=False, help_text="Send email only to preview user for testing."
    )
    include_ics = forms.BooleanField(
        required=False, help_text="Include latest meetup ICS invitation."
    )
