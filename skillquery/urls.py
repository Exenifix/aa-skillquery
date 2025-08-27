"""Routes."""

from django.urls import path

from . import views

app_name = "skillquery"

urlpatterns = [
    path("", views.index, name="index"),
    path("skill/", views.skill_analyzer, name="skill"),
    path("skillset/", views.skillset_analyzer, name="skillset"),
    path("api/skill_autocomplete", views.skill_autocomplete, name="api_skill_autocomplete"),
]
