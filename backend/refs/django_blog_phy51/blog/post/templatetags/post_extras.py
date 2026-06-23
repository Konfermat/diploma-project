from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def smart_time(value):
    if not value:
        return ""
    now = timezone.now()
    diff = now - value
    if diff < timedelta(hours=12):
        total_seconds = int(diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        if hours > 0:
            return f'{hours}ч. назад'
        return f'{minutes} мин. назад'
    if value.date() == now.date():
        return f'Сегодня в {value.strftime("%H:%M")}'

    if value.date() == now.date() - timedelta(days=1):
        return f'Вчера в {value.strftime("%H:%M")}'

    return f'{value.strftime("%d.%m.%Y %H:%M")}'