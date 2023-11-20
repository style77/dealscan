import json
import random
from datetime import datetime, timedelta

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django.views.generic import TemplateView

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class IndexView(TemplateView):
    template_name = "index/index.html"


class PricingView(TemplateView):
    template_name = "index/pricing.html"


def get_created_accounts_percentage() -> float:
    days_count = 7
    today = timezone.now()
    start_of_week = today - timedelta(days=days_count)
    prev_start_of_week = start_of_week - timedelta(days=days_count)

    users_created_last_week = User.objects.filter(
        date_joined__range=[start_of_week, today]
    ).count()
    users_created_prev_week = User.objects.filter(date_joined__range=[prev_start_of_week, start_of_week]).count()

    percentage_difference = (
        (users_created_last_week - users_created_prev_week) / (users_created_last_week + users_created_prev_week)
    ) * 100

    return percentage_difference


def get_formatted_sign(val: float) -> str:
    if val >= 0:
        return "+"
    else:
        return ""  # since negative values got minus before value itself


def dashboard_callback(request, context):
    current_date = datetime.now()
    WEEKS = [
        (current_date - timedelta(weeks=i)).strftime("%Y-%m-%d") for i in range(28)
    ][::-1]

    positive = [[1, random.randrange(8, 28)] for _ in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for _ in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for _ in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for _ in range(1, 28)]

    users_percentage = get_created_accounts_percentage()
    users_percentage_sign = get_formatted_sign(users_percentage)

    context.update(
        {
            "navigation": [
                {"title": _("Dashboard"), "link": "/admin", "active": True},
                {"title": _("Analytics"), "link": "/admin/analytics"},
                {"title": _("Settings"), "link": "/admin/settings"},
            ],
            "filters": [
                {"title": _("All"), "link": "#", "active": True},
                {
                    "title": _("New"),
                    "link": "#",
                },
            ],
            "kpi": [
                {
                    "title": "Created Accounts",
                    "metric": User.objects.count(),
                    "footer": mark_safe(
                        f'<strong class="{"text-green-600 font-medium" if users_percentage >= 0 else "text-red-600 font-medium"}">{users_percentage_sign}{users_percentage:.2f}%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": WEEKS,
                            "datasets": [{"data": average, "borderColor": "#9333ea"}],
                        }
                    ),
                },
                {
                    "title": "Product B Performance",
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                },
                {
                    "title": "Product C Performance",
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                },
            ],
            "progress": [
                {
                    "title": "Social marketing e-book",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Freelancing tasks",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Development coaching",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Product consulting",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
                {
                    "title": "Other income",
                    "description": " $1,234.56",
                    "value": random.randint(10, 90),
                },
            ],
            "chart": json.dumps(
                {
                    "labels": WEEKS,
                    "datasets": [
                        {
                            "label": "Example 1",
                            "type": "line",
                            "data": average,
                            "backgroundColor": "#bbf7d0",
                            "borderColor": "#bbf7d0",
                        },
                        {
                            "label": "Example 2",
                            "data": positive,
                            "backgroundColor": "#4ade80",
                        },
                        {
                            "label": "Example 3",
                            "data": negative,
                            "backgroundColor": "#166534",
                        },
                    ],
                }
            ),
            "performance": [
                {
                    "title": _("Last week revenue"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": WEEKS,
                            "datasets": [
                                {"data": performance_positive, "borderColor": "#4ade80"}
                            ],
                        }
                    ),
                },
                {
                    "title": _("Last week expenses"),
                    "metric": "$1,234.56",
                    "footer": mark_safe(
                        '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                    ),
                    "chart": json.dumps(
                        {
                            "labels": WEEKS,
                            "datasets": [
                                {"data": performance_negative, "borderColor": "#f43f5e"}
                            ],
                        }
                    ),
                },
            ],
        },
    )

    return context
