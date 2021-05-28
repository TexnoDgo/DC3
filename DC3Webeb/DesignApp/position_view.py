from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

from MainApp.models import *
from MainApp.handlers import *
from .component_view import *


# Создание новой позиции
def create_position(order_name, component, quantity, priority, assembly, username):
    try:
        # Получение заказ
        order = Order.objects.get(info__title=order_name)
        # Проверка существования компонента сборки
        m_assembly = component_is_real(assembly)
        # Если компонента сборки не существует - создать!
        if not m_assembly:
            # Получение пользователя
            user = User.objects.get(username=username)
            # Создание информации компонента сборки
            info = Info(title=assembly, author=user, p_class='COMPONENT')
            info.save()
            # Создание компонента сборки
            m_assembly = Component(info=info, c_type='ASSEMBLY', material='default', thickness='0', band_count='0')
            m_assembly.save()
        # Создание кода позиции
        code = get_random_string(length=13)
        # Генерация QR-кода производства
        pk_qr_code = generative_qr_code(code, 'PK')
        # Генерация QR-кода смарт
        smart_qr_code = generative_qr_code(code, 'SMART')
        # Создание позиции
        storage = StoragePlace.objects.get(title='A0')
        position = Position(order=order, component=component, quantity=quantity, priority=priority,
                            m_assembly=m_assembly, code=code, pk_prod_qr_code=pk_qr_code,
                            smart_prod_qr_code=smart_qr_code, storage=storage)

        position.save()
        # Если у компонента есть чертеж - Генерация модифицированного PDF
        if position.component.pdf_draw:
            pdf_draw = create_modify_draw(component=position.component, position=position, order=position.order,
                                          code=code)
            position.pdf_draw_wt_qr_code = pdf_draw
            position.save()
        return position
    except Exception:
        return False


# Проверка позиций входящих в проект
def position_chek(component, order):
    component = component_is_real(component)
    if component:
        order = Order.objects.get(info__title=order)
        positions = Position.objects.filter(order=order, component=component)
        return positions
    else:
        return False


# Проверка позиции входящей в заказ с сборкой
def position_pre_chek(position, order, assembly):
    try:
        assembly = Component.objects.get(info__title=assembly)
        order = Order.objects.get(info__title=order)
        position = Position.objects.get(order=order, m_assembly=assembly, component__info__title=position)
        if position:
            return True
        else:
            return False
    except Exception:
        return False


# Изминение кол-во компонентов в позиции
def position_edit(position, order, assembly, quantity):
    try:
        assembly = Component.objects.get(info__title=assembly)
        order = Order.objects.get(info__title=order)
        position = Position.objects.get(order=order, m_assembly=assembly, component__info__title=position)
        print('Кол-во позиций: ' + quantity)
        position.quantity = quantity
        position.save()
        return True
    except Exception:
        return False


# Удаление позиции
def position_delete(position, order, assembly):
    try:
        assembly = Component.objects.get(info__title=assembly)
        order = Order.objects.get(info__title=order)
        position = Position.objects.get(order=order, m_assembly=assembly, component__info__title=position)
        position.delete()
        return True
    except Exception:
        return False
