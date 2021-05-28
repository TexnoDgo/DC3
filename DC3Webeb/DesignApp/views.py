from random import random
from wsgiref.util import FileWrapper

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.http import HttpResponse

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from MainApp.models import *
from .info import *
from .component_view import *
from .position_view import *
from .order_view import *


# Тест
class GetRequestClass(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {}
        # request_types
        # get_active_order - получение активного заказа пользователя

        # Список получаемых переменных
        request_type = request.data["request_type"]
        username = request.data["username"]
        component_name = request.data["component_name"]
        component_type = request.data["component_type"]
        assembly = request.data["assembly"]
        material = request.data["material"]
        thickness = request.data["thickness"]
        band = request.data["band"]
        quantity = request.data["quantity"]
        operation = request.data["operation"]
        project_name = request.data["project_name"]
        project_name2 = request.data["project_name2"]
        device_name = request.data["device_name"]
        order_name = request.data["order_name"]
        order_name2 = request.data["order_name2"]
        priority = request.data["priority"]

        print('--------------------Вводные данные--------------------')
        print(request_type)
        print(username)
        print(component_name)
        print(component_type)
        print(assembly)
        print(material)
        print(thickness)
        print(band)
        print(quantity)
        print(operation)
        print(project_name)
        print(project_name2)
        print(device_name)
        print(order_name)
        print(order_name2)
        print(priority)
        print('------------------------------------------------------')

        # --------------------Информационные---------------------
        # Передача активного заказа для пользователя
        if request_type == "info":
            try:
                profile = info(username)
                active_project = profile.active_project
                project_device = active_project.device
                active_order = profile.active_order
                user = str(profile.user.username)
                active_project = str(active_project)
                project_device = str(project_device)
                active_order = str(active_order)
            except Exception:
                user = 'Пользователь не обраружен'
                active_project = 'Активный проект'
                project_device = 'Активное устройство'
                active_order = 'Активный заказ'
            data = {
                'user': user,
                'active_project': active_project,
                'project_device': project_device,
                'active_order': active_order,
            }
        # Передача списка устройств
        elif request_type == 'get_device_list':
            devices = device_list()
            i = 0
            for element in devices:
                data[i] = element.info.title
                i += 1
        # Передача списка проектов для устройства
        elif request_type == 'get_project_list_for_device':
            projects = project_list_for_device(device_name)
            if projects:
                i = 0
                for element in projects:
                    data[i] = element.info.title
                    i += 1
            else:
                data[0] = 'Проекты не обнаружены'
        # Передача списка заказов для проекта
        elif request_type == 'get_order_list_for_project':
            print(project_name)
            orders = order_list_for_project(project_name)
            if orders:
                i = 0
                for element in orders:
                    data[i] = element.info.title
                    i += 1
            else:
                data[0] = 'Заказы не обнаружены'
        # Передача списка первичных операций
        elif request_type == 'get_first_operation':
            operations = first_operations_list()
            if operations:
                i = 0
                for element in operations:
                    data[i] = element.title
                    i += 1
            else:
                data[0] = 'Операции отсутствуют'
        # Передача списка материалов
        elif request_type == 'get_material_list':
            materials = 0
        elif request_type == 'get_active_project_for_user':
            project = 0

        # -------------------Компоненты--------------------------
        # Предпроверка существования позиции в заказе с одинаковой сборкой
        elif request_type == 'position_pre_chek':
            p_p_c = position_pre_chek(component_name, order_name, assembly)
            position = position_pre_chek(component_name, order_name, assembly)
            if position:
                data[0] = 'True'
            else:
                data[0] = 'False'
            print(p_p_c)
        # Добавление позиции
        elif request_type == 'position_add':
            # Проверка существования компонента
            real_component = component_is_real(component_name)
            # Если компонент существует
            if real_component:
                component = real_component
            # Если комопнент не существует
            else:
                # Создать компоннет
                component = component_create(component_name, username, component_type, material, thickness,
                                             band)
            # Создать позицию с новым компонентом
            position = create_position(order_name, component, quantity, priority, assembly, username)
            position.save
        # Проверка существующих позиций в заказе
        elif request_type == 'position_chek':
            positions = position_chek(component_name, order_name)
            if positions:
                i = 0
                for position in positions:
                    mini_data = {'mather_assembly': position.m_assembly.info.title, 'quantity': position.quantity}
                    data[i] = mini_data
                    i += 1
        # Изминение кол-во компонентов в позиции
        elif request_type == 'position_edit':
            position = position_edit(component_name, order_name, assembly, quantity)
            if position:
                data[0] = 'True'
            else:
                data[0] = 'False'
        # Удаление позиции
        elif request_type == 'position_delete':
            position = position_delete(component_name, order_name, assembly)
            if position:
                data[0] = 'True'
            else:
                data[0] = 'False'

        # -----------------------Заказы-------------------------
        # Созданеи заказа
        elif request_type == 'order_create':
            order_is_real = order_chek(project_name, order_name)
            print(order_is_real)
            if order_is_real:
                data[0] = 'False'
            elif not order_is_real:
                order = order_crate2(project_name, order_name, username)
                if order:
                    data[0] = 'True'
                else:
                    data[0] = 'False'
        elif request_type == 'order_activate':
            order = order_activate(order_name, username)
            if order:
                data[0] = 'True'
            else:
                data[0] = 'False'
        return JsonResponse(data)


# TODO: Класс добавления файлов
# TODO: Отработать все функции добавления файлов
class AddFileToComponent(APIView):
    parser_classes = [FileUploadParser, JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer]

    def put(self, request, filename, format=None):
        try:
            file_obj = request.data['file']
            print(filename)
            print(filename[-7:-1])
            # Если DXF-файл
            if filename[-4:-1] == 'DXF' or filename[-4:-1] == 'dxf':
                print('addDXF')
                component_name = filename[:-5]
                component = Component.objects.get(title=component_name)
                component.draw_pdf = file_obj
                component.save()

            # Если PDF-файл
            elif filename[-4:-1] == 'PDF' or filename[-4:-1] == 'pdf':
                print('addPDF')
                component_name = filename[:-5]
                component = Component.objects.get(title=component_name)
                a = random()
                b = a * 10000000000000
                c = str(b)[:13]
                file_obj.name = c + ".PDF"
                component.draw_pdf = file_obj
                component.save()

            # Если файл Детали или сборки
            elif filename[-7:-1] == 'SLDPRT' or filename[-7:-1] == 'sldprt' or filename[-7:-1] == 'SLDASM' \
                    or filename[-7:-1] == 'sldasm':
                print('addSLDPRT')
                component_name = filename[:-8]
                print(component_name)
                component = Component.objects.get(title=component_name)
                component.part_file = file_obj
                component.save()

            return Response(True)
        except Exception:
            return Response(False)
