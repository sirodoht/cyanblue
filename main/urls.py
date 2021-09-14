from django.urls import path

from main import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:event_slug>/", views.event, name="event"),
    path("<slug:event_slug>/ics", views.event_ics, name="event_ics"),
    path(
        "dashboard/announce/",
        views.DashboardAnnounce.as_view(),
        name="dashboard_announce",
    ),
    path(
        "unsubscribe/<uuid:key>/",
        views.unsubscribe_key,
        name="unsubscribe_key",
    ),
    path("about/code-of-conduct/", views.coc, name="coc"),
]
