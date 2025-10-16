from collections import defaultdict
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.urls import reverse

from newsfox.core.models import Category
from newsfox.news.models import ArticlePage, ArticleTag, BreakingNews
from taggit.models import Tag


def load_news_context_data(request):
    articles = (
        ArticlePage.objects.live()
        .public()
        .select_related("category", "section")
        .prefetch_related("authors", "tags")
    )
    archives = (
        articles.exclude(published_at__isnull=True)
        .annotate(month=TruncMonth("published_at"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("-month")
    )

    context = {
        "latest_articles": articles.order_by("-published_at")[:10],
        "featured_articles": articles.filter(is_featured=True).order_by("?")[:2],
        "popular_articles": articles.order_by("-view_count", "?")[:2],
        "sticky_articles": articles.filter(is_sticky=True)[:3],
        "articles": articles,
    }
    context["archives"] = [
        {
            "month": archive["month"],
            "count": archive["count"],
            "url": reverse(
                "article_archive",
                kwargs={
                    "year": archive["month"].year,
                    "month": f"{archive['month'].month:02}",
                },
            ),
        }
        for archive in archives
    ]
    context["categories"] = Category.objects.all().order_by("?")[:7]
    # All tags used by those articles
    tag_ids = ArticleTag.objects.filter(content_object__in=articles).values_list(
        "tag_id", flat=True
    )

    # Aggregate tag usage counts
    context["tags"] = (
        Tag.objects.filter(id__in=tag_ids)
        .annotate(article_count=Count("id"))
        .order_by("-article_count", "name")
    )
    context["breaking_news"] = BreakingNews.objects.filter(is_active=True).order_by(
        "-id"
    )

    return context
