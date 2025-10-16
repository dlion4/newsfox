from collections import defaultdict
import random
from typing import Any
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from newsfox.core.models import Category
from newsfox.news.models import ArticlePage, Video
from django.utils import timezone

class NewsHomeView(TemplateView):
    """View to display a list of news articles."""

    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = (
            ArticlePage.objects.live()
            .public()
            .select_related("category")
            .order_by("?")[:6]
        )

        grouped_articles = defaultdict(list)
        grouped_articles = defaultdict(list)
        for article in articles:
            if article.category:
                grouped_articles[article.category].append(article)
        grouped_articles = dict(grouped_articles)
        category_items = list(grouped_articles.items())
        random.shuffle(category_items)
        grouped_articles = dict(category_items[:3])
        context["grouped_articles"] = dict(grouped_articles)
        all_articles = ArticlePage.objects.live().public()
        international_articles = all_articles.order_by("?")[:4]
        context["international_articles"] = international_articles
        context["videos"] = Video.objects.all().order_by("?")
        return context


def news_detail_view(request):
    """View to display a news article based on its slug."""
    # --- IGNORE ---
    return render(request, "pages/news/detail.html", {})


def category_view(request, category_slug):
    """View to display articles in a specific category."""
    category = get_object_or_404(Category, slug=category_slug)
    articles = (
        ArticlePage.objects.live()
        .public()
        .filter(category=category)
        .order_by("-published_at")
    )
    videos = Video.objects.all().order_by("?")[:3]
    return render(request, "pages/news/category.html", {
        "category": category,
        "articles": articles,
        "videos": videos,
    })
