from django import forms
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.fields import RichTextField
from wagtail.models import Orderable
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.admin.panels import FieldPanel



class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        "ArticlePage", related_name="tagged_items", on_delete=models.CASCADE
    )
    class Meta:
        verbose_name = "Article Tag"
        verbose_name_plural = "Article Tags"


class ArticlePage(Page):
    category = models.ForeignKey(
        "core.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    section = models.ForeignKey(
        "core.Section",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    cover = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    authors = ParentalManyToManyField("core.AuthorProfile", blank=True)
    tags = ClusterTaggableManager(through=ArticleTag, blank=True, related_name="article_tags")

    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    reading_time = models.IntegerField(null=True, blank=True)
    word_count = models.IntegerField(null=True, blank=True)
    language = models.CharField(
        max_length=10, default="en", choices=[("en", "English"), ("es", "Spanish")]
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_sticky = models.BooleanField(default=False, db_index=True)
    is_editors_pick = models.BooleanField(default=False, db_index=True)
    view_count = models.BigIntegerField(default=0, db_index=True)

    body = RichTextField(blank=True)
    summary = models.TextField(blank=True)
    content_panels = [
        *Page.content_panels,
        FieldPanel("category"),
        FieldPanel("section"),
        FieldPanel("published_at", read_only=True),
        FieldPanel("reading_time"),
        FieldPanel("word_count", read_only=True),
        FieldPanel("language", classname="w-full"),
        FieldPanel("is_featured"),
        FieldPanel("is_sticky"),
        FieldPanel("is_editors_pick"),
        FieldPanel("view_count", read_only=True),
        FieldPanel("body", classname="full"),
        FieldPanel("summary", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("authors", widget=forms.CheckboxSelectMultiple),
            ]
        ),
        "cover",
        "tags",
        "media_gallery",
    ]

    template = "pages/news/detail.html"
    @property
    def get_next_article(self):
        return (
            ArticlePage.objects.live()
            .public()
            .filter(first_published_at__gt=self.first_published_at)
            .order_by("first_published_at")
            .first()
        )
    @property
    def get_previous_article(self):
        return (
            ArticlePage.objects.live()
            .public()
            .filter(first_published_at__lt=self.first_published_at)
            .order_by("-first_published_at")
            .first()
        )
    def get_related_articles(self):
        return ArticlePage.objects.live().public().filter(
            models.Q(category=self.category) | models.Q(section=self.section)
        ).exclude(id=self.id).distinct().order_by("?")

class ArticleMediaGallery(Orderable):
    page = ParentalKey(
        ArticlePage, related_name="media_gallery", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(max_length=255, blank=True)
    panels = ["image", "caption"]



class Video(models.Model):
    """Simple video snippet for embedding YouTube/Vimeo videos."""

    title = models.CharField(max_length=255)
    video_url = models.URLField(help_text="Paste the YouTube or Vimeo video URL")
    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional: thumbnail image for this video",
    )
    category = models.ForeignKey(
        "core.Category",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="videos",
    )
    date_added = models.DateField(auto_now_add=True)



    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return self.title


class BreakingNews(models.Model):
    """Model to store breaking news items."""

    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]
        verbose_name = "Breaking News"
        verbose_name_plural = "Breaking News"

    def __str__(self):
        return self.title
