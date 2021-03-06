from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.open_entry, name="open_entry"),
    path("random/", views.random, name="random"),
    path("new/", views.new_entry, name="new"),
    path("search/", views.search, name="search"),
]
