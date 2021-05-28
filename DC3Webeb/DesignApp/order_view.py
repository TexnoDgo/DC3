from django.contrib.auth.models import User

from MainApp.models import *
from MainApp.handlers import *


# Проверка существующего заказ
def order_chek(project_name, order_name):
    try:
        project = Project.objects.get(info__title=project_name)
        order = Order.objects.get(info__title=order_name, project=project)
        return True
    except Exception:
        return False


# Создание нового заказа
def order_crate2(project_name, order_name, username):
    try:

        project = Project.objects.get(info__title=project_name)
        user = User.objects.get(username=username)
        print(user)
        info = Info(title=order_name, author=user, p_class="ORDER")
        info.save()
        order = Order(info=info, project=project, readiness="2020-01-01")
        order.save()
        return True
    except Exception:
        return False


# Активация заказа
def order_activate(order_name, username):
    try:
        order = Order.objects.get(info__title=order_name)
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        profile.active_order = order
        profile.active_project = order.project
        profile.save()
        return True
    except Exception:
        return False