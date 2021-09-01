from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:event_slug>/", views.event, name="event"),
]
