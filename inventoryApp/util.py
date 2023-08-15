from django.core.cache import cache


def invalidate_menu_cache(user_id, search_term=''):
    cache_key = f"menu_items_for_user_{user_id}_{search_term}"
    cache.delete(cache_key)
