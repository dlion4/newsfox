from django.urls import path
from django.views.generic import TemplateView

from .views import category_view, NewsHomeView

urlpatterns = [
    path("", NewsHomeView.as_view(), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("category/<slug:category_slug>/", category_view, name="category"),]
