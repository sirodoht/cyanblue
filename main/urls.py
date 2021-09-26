from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("<slug:event_slug>/", views.event, name="event"),
    path("<slug:event_slug>/ics/", views.event_ics, name="event_ics"),
    path(
        "dashboard/broadcast/",
        views.DashboardBroadcast.as_view(),
        name="dashboard_broadcast",
    ),
    path(
        "unsubscribe/<uuid:key>/",
        views.unsubscribe_key,
        name="unsubscribe_key",
    ),
    path("about/code-of-conduct/", views.coc, name="coc"),
]
