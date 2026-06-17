from functools import wraps
from cachetools import TTLCache
from aiogram.types import CallbackQuery

button_cooldown = TTLCache(maxsize=10000, ttl=2.0)


def rate_limit_button(rate_limit: float = 2.0):
    """
    Декоратор для ограничения нажатий на конкретную кнопку
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(callback: CallbackQuery, *args, **kwargs):
            user_id = callback.from_user.id
            # Используем комбинацию user_id + имя функции для уникальности
            cache_key = f"{user_id}_{func.__name__}"

            if cache_key in button_cooldown:
                await callback.answer(
                    f"⏳ Крутить можно раз в {rate_limit} секунд",
                    show_alert=True
                )
                return

            button_cooldown[cache_key] = True
            return await func(callback, *args, **kwargs)

        return wrapper

    return decorator
