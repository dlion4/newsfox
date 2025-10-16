import uuid

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class AuthorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(
        "users.Profile", on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=120)

    class Meta:
        indexes = [
            models.Index(fields=["display_name"]),
        ]

    def __str__(self):
        return self.profile.user.email


class Section(models.Model):
    """Optional grouping of categories / articles (e.g., News, Opinion)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    weight = models.IntegerField(default=0)  # ordering
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Hierarchical categories (self-referential)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    description = models.TextField(blank=True)
    section = models.ForeignKey(
        Section,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="categories",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Media(models.Model):
    """Store media metadata. Files will be in S3/Cloud storage; path in `file`."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.CharField(max_length=1024)  # path or URL
    mime_type = models.CharField(max_length=100, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    size = models.BigIntegerField(null=True, blank=True)
    author = models.ForeignKey(
        "users.Profile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_media",
    )
    alt_text = models.CharField(max_length=255, blank=True)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["mime_type"]),
        ]

    def __str__(self):
        return self.file


class Article(models.Model):
    """Main article object. Use as the single source of truth for published content."""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("review", "In Review"),
        ("scheduled", "Scheduled"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(
        max_length=255, unique=True
    )
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)  # short excerpt
    body = models.TextField(blank=True)  # HTML or markdown
    body_markdown = models.TextField(blank=True)  # optional: original markdown
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", db_index=True
    )
    canonical_url = models.CharField(
        max_length=1024, blank=True, help_text="If this article is syndicated"
    )
    author = models.ForeignKey(
        AuthorProfile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    co_authors = models.ManyToManyField(
        AuthorProfile, blank=True, related_name="coauthored_articles"
    )
    editors = models.ManyToManyField(
        AuthorProfile, blank=True, related_name="edited_articles"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")
    section = models.ForeignKey(
        Section,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="articles",
    )
    primary_image = models.ForeignKey(
        Media, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    scheduled_at = models.DateTimeField(null=True, blank=True, db_index=True)
    reading_time = models.IntegerField(null=True, blank=True)  # minutes (computed)
    word_count = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=10, default="en")
    seo = models.JSONField(default=dict, blank=True)  # title, meta desc, schema, og
    custom_fields = models.JSONField(default=dict, blank=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_sticky = models.BooleanField(default=False, db_index=True)
    view_count = models.BigIntegerField(
        default=0, db_index=True
    )  # denormalized, but indexed
    comment_count = models.IntegerField(default=0)
    reading_history = models.JSONField(
        default=list, blank=True
    )  # optional: store last X viewers (careful)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # full text search vector column (managed by trigger)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["is_featured", "published_at"]),
            GinIndex(fields=["search_vector"]),  # Postgres tsvector GIN index
        ]

    def __str__(self):
        return self.title


class ArticleRevision(models.Model):
    """Keep full history of article edits (can store delta or full copy)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="revisions"
    )
    author = models.ForeignKey(AuthorProfile, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=500)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    body_markdown = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_snapshot = models.BooleanField(
        default=False
    )  # snapshot of published state

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Threaded comments; you might offload to external comment system for scale."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(
        "users.Profile", null=True, blank=True, on_delete=models.SET_NULL
    )
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    body = models.TextField()
    is_visible = models.BooleanField(default=True)
    is_spam = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["article", "created_at"]),
        ]

    def __str__(self):
        return self.article.title


class Reaction(models.Model):
    """Generic reaction: like, bookmark, clap, etc.
    Use content_type for polymorphism if needed."""

    REACTION_CHOICES = [
        ("like", "Like"),
        ("bookmark", "Bookmark"),
        ("clap", "Clap"),
        ("upvote", "Upvote"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="reactions"
    )
    article = models.ForeignKey(
        Article,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    comment = models.ForeignKey(
        Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reactions",
    )
    kind = models.CharField(max_length=30, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "article", "comment", "kind")

    def __str__(self):
        return self.article.title


class EditorialAssignment(models.Model):
    """Track assignments & workflow"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="assignments"
    )
    assigned_by = models.ForeignKey(
        AuthorProfile, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    assignee = models.ForeignKey(
        AuthorProfile, null=True, on_delete=models.SET_NULL, related_name="+"
    )
    status = models.CharField(max_length=50, default="assigned")
    notes = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article.title


class PublishLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    performed_by = models.ForeignKey(
        AuthorProfile, null=True, on_delete=models.SET_NULL
    )
    action = models.CharField(max_length=50)  # publish/unpublish/update
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.article.title


class Redirect(models.Model):
    """SEO-friendly redirects."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_path = models.CharField(max_length=1024, unique=True)
    to_path = models.CharField(max_length=1024)
    http_status = models.IntegerField(default=301)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_path} >> {self.to_path}"
