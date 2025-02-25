
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("<int:year>/<str:month>/", views.index, name="index"),
    path("events", views.all_events, name='events'),
    path("add_vanue", views.add_vanue, name='add_vanue'),
    path("vanue", views.vanue, name='vanue'),
    path("vanue/<int:id>", views.show_vanue, name='show_vanue'),
    path("search", views.search, name='search'),
    path('update_vanue/<int:id>', views.update_vanue, name='update_vanue'),
    path('update_event/<int:id>', views.update_event, name='update_event'),
    path("add_event", views.add_event, name='add_event'),
    path("delete_event/<int:id>", views.delete_event, name='delete_event'),
    path("delete_vanue/<int:id>", views.delete_vanue, name='delete_vanue'),
    path('vanue_text', views.vanue_text, name='vanue_text'),
    path("vanue_csv", views.vanue_csv, name='vanue_csv'),
    path('vanue_pdf', views.vanue_pdf, name='vanue_pdf'),
    path('search_event', views.search_event, name='search_event'),
    path('admin', views.admin, name='admin'),
    path('vanue_events/<int:vanue_id>', views.vanue_events, name='vanue_events'),
    path('show_event/<int:event_id>', views.show_event, name='show_event'),
]