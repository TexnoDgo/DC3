from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.http import HttpResponse

from .forms import *
from .handlers import *


# ДОМАШНЯЯ СТРАНИЦА
def index(request):
    return render(request, 'MainApp/index.html')


# Класс Компонентов
class ComponentClass:
    # Функция создания нового компонента
    @login_required  # Только для аутенфицированных поьлзователей
    def component_create(request):
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST)
            component_form = ComponentCreateForm(request.POST, request.FILES)
            if info_form.is_valid() and component_form.is_valid():
                # TODO: добавить проверку уникальности информационного названия - DONE!
                # Создание информации
                info = info_form.save(commit=False)
                info.author = request.user
                info.p_class = "COMPONENT"
                info.save()
                component = component_form.save(commit=False)
                component.info = info
                component.save()
                # TODO: добавить функцию изминения pdf в png - DONE!
                if component.pdf_draw:
                    png_draw = convert_pdf_to_png(component.pdf_draw)
                    component.png_draw = png_draw
                component.save()
                return redirect('component_view_all')

        else:
            info_form = InfoCreateForm()
            component_form = ComponentCreateForm()
        context = {
            'info_form': info_form,
            'component_form': component_form,
        }
        return render(request, 'MainApp/Component/component_create.html', context)

    # Функция просмотра компонента
    def component_view(request, pk):
        component = Component.objects.get(pk=pk)
        context = {
            'component': component,
        }
        return render(request, 'MainApp/Component/component_view.html', context)

    # Функция редактирвоания компонента
    @login_required  # Только для аутенфицированных поьлзователей
    def component_edit(request, pk):
        component = Component.objects.get(pk=pk)
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST, instance=component.info)
            component_form = ComponentCreateForm(request.POST, request.FILES, instance=component)
            if info_form.is_valid() and component_form.is_valid():
                info_form.save()
                component_form.save()
                # TODO: доработать функцию конвертации и сохраенния png чертежа после обновления компонента - DONE!
                png_draw = convert_pdf_to_png(component.pdf_draw)
                component.png_draw = png_draw
                component.save()
                return redirect('component_view', pk=component.pk)
        else:
            info_form = InfoCreateForm(instance=component.info)
            component_form = ComponentCreateForm(instance=component)

        context = {
            'component': component,
            'info_form': info_form,
            'component_form': component_form,
        }

        return render(request, 'MainApp/Component/component_edit.html', context)

    # Функция просмотра ВСЕХ компонентов
    def component_view_all(request):
        components = Component.objects.all()
        context = {
            'components': components,
        }
        return render(request, 'MainApp/Component/component_view_all.html', context)


# Класс Устройств
class DeviceClass:
    # Функция создания нового устройства
    @login_required  # Только для аутенфицированных поьлзователей
    def device_create(request):
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST)
            if info_form.is_valid():
                info = info_form.save(commit=False)
                info.author = request.user
                info.p_class = "DEVICE"
                device = Device(info=info)
                info.save()
                device.save()
                return redirect('device_view_all')
        else:
            info_form = InfoCreateForm()

        context = {
            'info_form': info_form,
        }
        return render(request, 'MainApp/Device/device_create.html', context)

    # Функция просмотра ВСЕ устройств
    def device_view_all(request):
        devices = Device.objects.all()
        context = {
            'devices': devices,
        }
        return render(request, 'MainApp/Device/device_view_all.html', context)

    # Функция просмотра устройства
    def device_view(request, pk):
        device = Device.objects.get(pk=pk)
        projects = Project.objects.filter(device=device)
        context = {
            'device': device,
            'projects': projects,
        }
        return render(request, 'MainApp/Device/device_view.html', context)

    # Функция редактирования устройства
    @login_required  # Только для аутенфицированных поьлзователей
    def device_edit(request, pk):
        device = Device.objects.get(pk=pk)
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST, instance=device.info)
            if info_form.is_valid():
                info = info_form.save(commit=False)
                info.save()
                return redirect('device_view', pk=device.pk)
        else:
            info_form = InfoCreateForm(instance=device.info)

        context = {
            'info_form': info_form,
        }

        return render(request, 'MainApp/Device/device_edit.html', context)


# Класс Проектов
class ProjectClass:
    # Функция создания проекта
    @login_required  # Только для аутенфицированных поьлзователей
    def project_create(request):
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST)
            project_form = ProjectCreateForm(request.POST)
            if project_form.is_valid() and info_form.is_valid():
                info = info_form.save(commit=False)
                info.author = request.user
                info.p_class = "PROJECT"
                info.save()
                project = project_form.save(commit=False)
                project.info = info
                project.save()
                return redirect('project_view_all')
        else:
            info_form = InfoCreateForm()
            project_form = ProjectCreateForm()

        context = {
            'info_form': info_form,
            'project_form': project_form,
        }
        return render(request, 'MainApp/Project/project_create.html', context)

    # Функция просмотра проекта
    def project_view(request, pk):
        project = Project.objects.get(pk=pk)
        orders = Order.objects.filter(project=project)
        context = {
            'project': project,
            'orders': orders,
        }
        return render(request, 'MainApp/Project/project_view.html', context)

    # Функция просмотра ВСЕХ проектов
    def project_view_all(request):
        projects = Project.objects.all()
        context = {
            'projects': projects,
        }
        return render(request, 'MainApp/Project/project_view_all.html', context)

    # Функция просмотра сборок проекта со всеми в нее входящими
    def project_assembly(request, pk):
        project = Project.objects.get(pk=pk)
        m_positions = []
        orders_positions = []
        orders = Order.objects.filter(project=project)

        for order in orders:
            positions = Position.objects.filter(order=order)
            for position in positions:
                orders_positions.append(position)
                if position.component.c_type == 'ASSEMBLY':
                    m_positions.append(position)

        context = {
            'project': project,
            'm_positions': m_positions,
            'orders': orders,
            #'positions': positions,
            'orders_positions': orders_positions,
        }

        return render(request, 'MainApp/Project/project_assembly.html', context)

    # Функция формирования таблицы спецификации для проекта и сборки проекта
    def project_specification(request, pk, a_type, m_position_pk):
        project = Project.objects.get(pk=pk)
        if a_type == 'ASSEMBLY':

            pass
        elif a_type == 'PROJECT':
            m_position = Position.objects.get(pk=m_position_pk)
            archive_path = specification_table(m_position, project)
            print(archive_path)
            archive_name = 'project_spec_archive_#{}_assembly_#{}.zip'.format(str(project.pk),
                                                                              str(m_position.component.pk))
            print(archive_name)

        with open(archive_path, 'rb') as ft:
            response = HttpResponse(ft.read(), content_type="application/x-zip-compressed")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(archive_name)
            return response

    # Функция редактирования проекта
    @login_required  # Только для аутенфицированных поьлзователей
    def project_edit(request, pk):
        project = Project.objects.get(pk=pk)
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST, instance=project.info)
            project_form = ProjectCreateForm(request.POST, instance=project)
            if info_form.is_valid() and project_form.is_valid():
                info_form.save()
                project_form.save()
                return redirect('project_view', pk=project.pk)
        else:
            info_form = InfoCreateForm(instance=project.info)
            project_form = ProjectCreateForm(instance=project)

        context = {
            'info_form': info_form,
            'project_form': project_form,
        }
        return render(request, 'MainApp/Project/project_edit.html', context)


# Класс Заказов
class OrderClass:
    # Функция создания заказа
    def order_create(request):
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST)
            order_form = OrderCreateForm(request.POST)
            if info_form.is_valid() and order_form.is_valid():
                info = info_form.save(commit=False)
                info.author = request.user
                info.p_class = 'ORDER'
                info.save()
                order = order_form.save(commit=False)
                order.info = info
                order.save()
                return redirect('order_view_all')
        else:
            info_form = InfoCreateForm()
            order_form = OrderCreateForm()

        context = {
            'info_form': info_form,
            'order_form': order_form,
        }
        return render(request, 'MainApp/Order/order_create.html', context)

    # Функция просмотра заказа
    def order_view(request, pk):
        order = Order.objects.get(pk=pk)
        positions = Position.objects.filter(order=order)
        if request.method == 'POST':
            form = PositionCreateFormForOrder(request.POST)
            if form.is_valid():
                position = form.save(commit=False)
                # Назначение заказа позиции текущим заказом
                position.order = order
                # Генерация случайного кода позиции
                code = get_random_string(length=13)
                position.code = code
                # Создание производственного QR-кода
                pk_qr_code = generative_qr_code(code, 'PK')
                position.pk_prod_qr_code = pk_qr_code
                # Создание смарт QR-кода
                smart_qr_code = generative_qr_code(code, 'SMART')
                position.smart_prod_qr_code = smart_qr_code
                # Модицикация чертежа компонента
                if position.component.pdf_draw:
                    pdf_draw = create_modify_draw(component=position.component, position=position, order=position.order,
                                                  code=code)
                    position.pdf_draw_wt_qr_code = pdf_draw
                position.save()
                return redirect('order_view', pk=order.pk)
        else:
            form = PositionCreateFormForOrder()
        context = {
            'order': order,
            'positions': positions,
            'form': form,
        }
        return render(request, 'MainApp/Order/order_view.html', context)

    # Функция просмотра ВСЕХ заказов
    def order_view_all(request):
        orders = Order.objects.all()
        context = {
            'orders': orders,
        }
        return render(request, 'MainApp/Order/order_view_all.html', context)

    # Функция редактирования заказа
    @login_required  # Только для аутенфицированных поьлзователей
    def order_edit(request, pk):
        order = Order.objects.get(pk=pk)
        if request.method == 'POST':
            info_form = InfoCreateForm(request.POST, instance=order.info)
            order_form = OrderCreateForm(request.POST, instance=order)
            if info_form.is_valid() and order_form.is_valid():
                info_form.save()
                order_form.save()
                return redirect('order_view', pk=order.pk)
        else:
            info_form = InfoCreateForm(instance=order.info)
            order_form = OrderCreateForm(instance=order)

        context = {
            'info_form': info_form,
            'order_form': order_form,
        }

        return render(request, 'MainApp/Order/order_edit.html', context)


# Класс Позиций
class PositionClass:
    # Функция создания позиции
    def position_create(request):
        if request.method == 'POST':
            position_form = PositionCreateForm(request.POST)
            if position_form.is_valid():
                position = position_form.save(commit=False)
                # TODO: добавить функцию генерации кода - DONE!
                code = get_random_string(length=13)
                position.code = code
                # TODO: добавить функцию создания QR-кода производства ПК - DONE!
                pk_qr_code = generative_qr_code(code, 'PK')
                position.pk_prod_qr_code = pk_qr_code
                # TODO: добавить функцию создания QR-кода производства SMART - DONE!
                smart_qr_code = generative_qr_code(code, 'SMART')
                position.smart_prod_qr_code = smart_qr_code
                # TODO: добавить функцию создания чертежа с QR-кодами и информацией - DONE! доработать
                if position.component.pdf_draw:
                    pdf_draw = create_modify_draw(component=position.component, position=position, order=position.order,
                                                  code=code)
                    position.pdf_draw_wt_qr_code = pdf_draw
                # TODO: добавить ограничеение на выбираемую материнскую сборку, только ASSEMBLY
                position.save()
                # TODO: добавить редирект на список позиций - DONE!
                return redirect('position_view_all')
        else:
            position_form = PositionCreateForm()

        context = {
            'position_form': position_form,
        }
        return render(request, 'MainApp/Position/position_create.html', context)

    # Функция просмотра позиции
    def position_view(request, pk):
        position = Position.objects.get(pk=pk)
        anassociations = AnAssociation.objects.filter(position=position)
        # Форма создания объединения операции и позиции
        if request.method == 'POST':
            form = AnAssociationCreateForm(request.POST)
            if form.is_valid():
                anassociation = form.save(commit=False)
                anassociation.position = position
                anassociation.status = 'CREATE'
                anassociation.save()
                return redirect('position_view', pk=position.pk)
        else:
            form = AnAssociationCreateForm()
        context = {
            'position': position,
            'form': form,
            'anassociations': anassociations,
        }
        return render(request, 'MainApp/Position/position_view.html', context)

    # Функция просмотра ВСЕХ позиций
    def position_view_all(request):
        positions = Position.objects.all()
        context = {
            'positions': positions,
        }
        return render(request, 'MainApp/Position/position_view_all.html', context)

    # Функция редактирования позиции
    @login_required  # Только для аутенфицированных поьлзователей
    def position_edit(request, pk):
        position = Position.objects.get(pk=pk)
        if request.method == 'POST':
            position_form = PositionCreateForm(request.POST, instance=position)
            if position_form.is_valid():
                # TODO: Добавить функцию изминения PDF чертежа позиции после изминения позиции
                position_form.save()
                return redirect('position_view', pk=position.pk)
        else:
            position_form = PositionCreateForm(instance=position)

        context = {
            'position': position,
            'position_form': position_form,
        }
        return render(request, 'MainApp/Position/position_edit.html', context)


# Класс Изготовитель
class ManufacturerClass:
    # Функция создания Изготовителя
    def manufacturer_create(request):
        if request.method == 'POST':
            form = ManufacturerCreateForm(request.POST)
            if form.is_valid():
                manufacturer = form.save(commit=False)
                manufacturer.save()
                return redirect('manufacturer_view_all')
        else:
            form = ManufacturerCreateForm()

        context = {
            'form': form,
        }

        return render(request, 'MainApp/Manufacturer/manufacturer_create.html', context)

    # Функция просмотра Изготовителя
    def manufacturer_view(request, pk):
        manufacturer = Manufacturer.objects.get(pk=pk)
        operations = Operation.objects.filter(manufacturer=manufacturer)
        context = {
            'manufacturer': manufacturer,
            'operations': operations,
        }
        return render(request, 'MainApp/Manufacturer/manufacturer_view.html', context)

    # Функция просмотра всех Изготовителей
    def manufacturer_view_all(request):
        manufacturers = Manufacturer.objects.all()
        context = {
            'manufacturers': manufacturers,
        }
        return render(request, 'MainApp/Manufacturer/manufacturer_view_all.html', context)

    # Функция редактировани Изготовителя
    @login_required  # Только для аутенфицированных поьлзователей
    def manufacturer_edit(request, pk):
        manufacturer = Manufacturer.objects.get(pk=pk)
        if request.method == 'POST':
            form = ManufacturerCreateForm(request.POST, instance=manufacturer)
            if form.is_valid():
                form.save()
                return redirect('manufacturer_view', pk=manufacturer.pk)

        else:
            form = ManufacturerCreateForm(instance=manufacturer)

        context = {
            'manufacturer': manufacturer,
            'form': form,
        }

        return render(request, 'MainApp/Manufacturer/manufacturer_edit.html', context)


# Класс Операции
class OperationClass:
    # Функция создания операции
    def operation_create(request):
        if request.method == 'POST':
            form = OperationCreateForm(request.POST)
            if form.is_valid():
                form.save()
                #TODO: исправить редирект
                return redirect('operation_view_all')
        else:
            form = OperationCreateForm()

        context = {
            'form': form,
        }

        return render(request, 'MainApp/Operation/operation_create.html', context)

    # Функция просмотра операции
    def operation_view(request, pk):
        operation = Operation.objects.get(pk=pk)
        context = {
            'operation': operation,
        }
        return render(request, 'MainApp/Operation/operation_view.html', context)

    # Функция просмотра ВСЕХ операций
    def operation_view_all(request):
        operations = Operation.objects.all()
        context = {
            'operations': operations,
        }
        return render(request, 'MainApp/Operation/operation_view_all.html', context)

    # Функция редактирования операции
    @login_required  # Только для аутенфицированных поьлзователей
    def operation_edit(request, pk):
        operation = Operation.objects.get(pk=pk)
        if request.method == 'POST':
            form = OperationCreateForm(request.POST, instance=operation)
            if form.is_valid():
                form.save()
                return redirect('operation_view', pk=operation.pk)
        else:
            form = OperationCreateForm(instance=operation)

        context = {
            'form': form,
            'operation': operation,
        }

        return render(request, 'MainApp/Operation/operation_edit.html', context)

    # Функция просмотра операции для изготовителя
    '''def operation_for_manufacturer(request, pk):
        manufacturer = Manufacturer.objects.get(pk=pk)
        operations = Operation.objects.filter(manufacturer=manufacturer)
        context = {
            'manufacturer': manufacturer,
            'operations': operations,
        }

        return render(request, 'MainApp/Operation/operation_for_manufacturer.html', context)'''


# Класс объединения
class AnAssociationClass:
    # Функции изминения статуса объединения
    def anassociation_status_edit(request, pk, new_status):
        anassociation = AnAssociation.objects.get(pk=pk)
        if request.method == 'GET':
            if new_status == 'CREATE':
                anassociation.status = 'CREATE'
            elif new_status == 'WORK':
                anassociation.status = 'WORK'
            elif new_status == 'DONE':
                anassociation.status = 'DONE'
            else:
                print('Ошибка изминения статуса для объединения')
        anassociation.save()
        return redirect('position_view', pk=anassociation.position.pk)

    # Функция удаления объединения
    @login_required  # Только для аутенфицированных поьлзователей
    def anassociation_delete(request, pk):
        anassociation = AnAssociation.objects.get(pk=pk)
        position = anassociation.position
        if request.method == 'GET':
            anassociation.delete()
        return redirect('position_view', pk=position.pk)
