from MainApp.models import *


# Получение информации проекта, устиройства, заказа пользователя
def info(username):
    try:
        profile = Profile.objects.get(user__username=username)
        return profile
    except Exception:
        return False


# Получение списка устройств
def device_list():
    try:
        devices = Device.objects.all()
        return devices
    except Exception:
        return False


# Получение списка проектов для устройства
def project_list_for_device(device_name):
    try:
        device = Device.objects.get(info__title=device_name)
        projects = Project.objects.filter(device=device)
        return projects
    except Exception:
        return False


# Получение списка заказов для проекта
def order_list_for_project(project_name):
    try:
        project = Project.objects.get(info__title=project_name)
        print(project)
        orders = Order.objects.filter(project=project)
        print(orders)
        return orders
    except Exception:
        return False


# Получение списка перевых операций
def first_operations_list():
    operations = Operation.objects.filter(priority=0)
    return operations


# Получение списка материалов
def get_material_list():
    pass
