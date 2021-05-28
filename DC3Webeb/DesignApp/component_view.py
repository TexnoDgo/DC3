from MainApp.models import *
from django.contrib.auth.models import User


# Функция проверки существования компонента
def component_is_real(component_name):
    try:
        component = Component.objects.get(info__title=component_name)
        return component
    except Exception:
        return False


# Функция создания компонента
def component_create(component_name, username, component_type, material, thickness, band):
    # Создание информации
    user = User.objects.get(username=username)
    component_info = Info(title=component_name, author=user, p_class='COMPONENT')
    component_info.save()
    # Создание компонента
    component = Component(info=component_info, c_type=component_type, material=material, thickness=thickness,
                          band_count=band)
    component.save()
    return component
