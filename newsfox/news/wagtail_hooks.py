from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from newsfox.core.models import Category, Section, AuthorProfile
from newsfox.news.models import Video, BreakingNews
from django.db import models


class CategoryViewSet(SnippetViewSet):
    model = Category
    menu_label = "Categories"
    menu_icon = "list-ul"
    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("description"),
        FieldPanel("section"),
        FieldPanel("parent"),
    ]


class SectionViewSet(SnippetViewSet):
    model = Section
    menu_label = "Sections"
    menu_icon = "folder-open-inverse"
    panels = [
        FieldPanel("title"),
        FieldPanel("slug"),
        FieldPanel("description"),
    ]


class AuthorProfileViewSet(SnippetViewSet):
    model = AuthorProfile
    menu_label = "Author Profiles"
    menu_icon = "user"
    panels = [
        FieldPanel("profile"),
        FieldPanel("display_name"),
    ]


class VideoViewSet(SnippetViewSet):
    model = Video
    menu_label = "Videos"
    panels = [
        FieldPanel("title"),
        FieldPanel("video_url"),
        FieldPanel("thumbnail"),
        FieldPanel("category"),
    ]

class BreakingNewsViewSet(SnippetViewSet):
    model = BreakingNews
    menu_label = "Breaking News"
    menu_icon = "warning"
    panels = [
        FieldPanel("title"),
        FieldPanel("url"),
        FieldPanel("is_active"),
    ]

register_snippet(CategoryViewSet)
register_snippet(SectionViewSet)
register_snippet(AuthorProfileViewSet)
register_snippet(VideoViewSet)
register_snippet(BreakingNewsViewSet)

