from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Article
from .models import ArticleRevision
from .models import AuthorProfile
from .models import Category
from .models import Comment
from .models import EditorialAssignment
from .models import Media
from .models import PublishLog
from .models import Reaction
from .models import Redirect
from .models import Section
from .models import Tag


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "profile")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "section", "slug")
    search_fields = ("title", "slug")
    list_filter = ("section",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("title",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "weight")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "file",
        "mime_type",
        "width",
        "height",
        "size",
        "author",
        "created_at",
    )
    search_fields = ("file",)
    list_filter = ("mime_type",)
    raw_id_fields = ("author",)
    readonly_fields = ("created_at",)


class ArticleRevisionInline(admin.TabularInline):
    model = ArticleRevision
    extra = 0
    readonly_fields = ("title", "created_at")
    can_delete = False


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author_display",
        "status",
        "published_at",
        "is_featured",
        "view_count",
    )
    list_filter = ("status", "is_featured", "is_sticky", "section", "category", "tags")
    search_fields = ("title", "slug", "summary", "body")
    raw_id_fields = (
        "author",
        "primary_image",
    )
    readonly_fields = ("created_at", "updated_at", "view_count", "comment_count")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    inlines = [ArticleRevisionInline]
    filter_horizontal = ("tags", "co_authors", "editors")

    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "body", "body_markdown")}),
        ("Authors & Editors", {"fields": ("author", "co_authors", "editors")}),
        (
            "Publication",
            {
                "fields": (
                    "status",
                    "scheduled_at",
                    "published_at",
                    "is_featured",
                    "is_sticky",
                    "reading_time",
                    "word_count",
                )
            },
        ),
        ("Relations", {"fields": ("section", "category", "tags", "primary_image")}),
        ("SEO", {"fields": ("seo", "canonical_url")}),
        ("Stats", {"fields": ("view_count", "comment_count")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def author_display(self, obj):
        if obj.author:
            return format_html(
                "<a href='{}'>{}</a>",
                reverse("admin:app_authorprofile_change", args=[obj.author.pk]),
                obj.author.display_name,
            )
        return "-"

    author_display.short_description = "Author"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "short_body",
        "article",
        "user",
        "is_visible",
        "is_spam",
        "created_at",
    )
    list_filter = ("is_visible", "is_spam")
    search_fields = ("body", "user__username", "article__title")
    raw_id_fields = ("article", "user")
    readonly_fields = ("created_at", "updated_at")

    def short_body(self, obj):
        return obj.body[:80]


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("user", "kind", "article", "comment", "created_at")
    list_filter = ("kind",)
    search_fields = ("user__username", "article__title")


@admin.register(EditorialAssignment)
class EditorialAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "assignee",
        "assigned_by",
        "status",
        "due_date",
        "created_at",
    )
    raw_id_fields = ("article", "assignee", "assigned_by")
    list_filter = ("status",)


@admin.register(PublishLog)
class PublishLogAdmin(admin.ModelAdmin):
    list_display = ("article", "performed_by", "action", "timestamp")
    readonly_fields = ("timestamp", "details")


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ("from_path", "to_path", "http_status")
    search_fields = ("from_path", "to_path")
