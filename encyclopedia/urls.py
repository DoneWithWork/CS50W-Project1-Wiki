from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:content>", views.content, name="content"),
    path("search/", views.search, name="search"),
    path("new/", views.NewPage, name="newpage"),
    path("edit/<str:title>", views.edit, name="editpage"),
    path("edit/<str:title>", views.edit, name="editpage"),
    path("random/", views.randomPage, name="random"),
]
