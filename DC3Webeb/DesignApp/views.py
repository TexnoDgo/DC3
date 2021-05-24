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

from .info import *


# Тест
class GetInfoClass(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = {}
        # request_types
        # get_active_order - получение активного заказа пользователя

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

        # Получение активного заказа для пользователя
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
        return JsonResponse(data)
