from MainApp.models import *


# Получение информации проекта, устиройства, заказа пользователя
def info(username):
    try:
        profile = Profile.objects.get(user__username=username)
        return profile
    except Exception:
        return False