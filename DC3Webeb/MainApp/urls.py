from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    # Страница создания Компонента
    path('component/create', ComponentClass.component_create, name='component_create'),
    # Страница просмотра комопнента
    path('component/view/<slug:pk>', ComponentClass.component_view, name='component_view'),
    # Страница редактирования компонента
    path('component/edit/<slug:pk>', ComponentClass.component_edit, name='component_edit'),
    # Страница просмотра ВСЕХ компонентов
    path('component/view_all', ComponentClass.component_view_all, name='component_view_all'),

    # Страница создания устройства
    path('device/create', DeviceClass.device_create, name='device_create'),
    # Страница просмотра ВСЕХ устройств
    path('device/view_all', DeviceClass.device_view_all, name='device_view_all'),
    # Страница просмотра устройства
    path('device/view/<slug:pk>', DeviceClass.device_view, name='device_view'),
    # Страница редактирования устройства
    path('device/edit/<slug:pk>', DeviceClass.device_edit, name='device_edit'),

    # Страница создания проекта
    path('project/create', ProjectClass.project_create, name='project_create'),
    # Страница просмотра проекта
    path('project/view/<slug:pk>', ProjectClass.project_view, name='project_view'),
    # Страница просмотра ВСЕХ проектов
    path('project/view_all', ProjectClass.project_view_all, name='project_view_all'),
    # Страница редактирования проекта
    path('project/edit/<slug:pk>', ProjectClass.project_edit, name='project_edit'),
    # Страница просмотра сборок проекта и из позиций
    path('project/assembly/<slug:pk>', ProjectClass.project_assembly, name='project_assembly'),
    # Ссылка формирования файла спецификации проекта или сборки
    path('project/specification/<slug:pk>/<a_type>/<m_position_pk>', ProjectClass.project_specification,
         name='project_specification'),

    # Страница создания заказа
    path('order/create', OrderClass.order_create, name='order_create'),
    # Страница просмотра заказа
    path('order/view/<slug:pk>', OrderClass.order_view, name='order_view'),
    # Страница просмотра ВСЕХ заказов
    path('order/view_all', OrderClass.order_view_all, name='order_view_all'),
    # Страница редактирования заказа
    path('order/edit/<slug:pk>', OrderClass.order_edit, name='order_edit'),

    # Страница создания позиции
    path('position/create', PositionClass.position_create, name='position_create'),
    # Страница просмотра позиции
    path('position/view/<slug:pk>', PositionClass.position_view, name='position_view'),
    # Страница просмотра ВСЕХ позиций
    path('position/view_all', PositionClass.position_view_all, name='position_view_all'),
    # Страница редактирования позиции
    path('position/edit/<slug:pk>', PositionClass.position_edit, name='position_edit'),

    # Страница создания изготовителя
    path('manufacturer/create', ManufacturerClass.manufacturer_create, name='manufacturer_create'),
    # Страница просмотра изготовителя
    path('manufacturer/view/<slug:pk>', ManufacturerClass.manufacturer_view, name='manufacturer_view'),
    # Страница просмотра ВСЕХ изготовителей
    path('manufacturer/view_all', ManufacturerClass.manufacturer_view_all, name='manufacturer_view_all'),
    # Страница редактирования изготовителя
    path('manufacturer/edit/<slug:pk>', ManufacturerClass.manufacturer_edit, name='manufacturer_edit'),

    # Страница создания операции
    path('operation/create', OperationClass.operation_create, name='operation_create'),
    # Страница просмотра операции
    path('operation/view/<slug:pk>', OperationClass.operation_view, name='operation_view'),
    # Страница просмотра ВСЕХ операций
    path('operation/view_all', OperationClass.operation_view_all, name='operation_view_all'),
    # Страница редактированяи операций
    path('operation/edit/<slug:pk>', OperationClass.operation_edit, name='operation_edit'),
    # Страница просмотра операции для изготовителя
    #path('operation/view_for_manufacturer/<slug:pk>', OperationClass.operation_for_manufacturer,
    #     name='operation_view_for_manufacturer'),

    # Методы изминения статуса для объединения
    path('anassociation/status/<slug:pk>/<new_status>', AnAssociationClass.anassociation_status_edit,
         name='anassociation_status_edit'),
    # Метод удаления объединения
    path('anassociation/delete/<slug:pk>', AnAssociationClass.anassociation_delete, name='anassociation_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
