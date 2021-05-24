from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


# Форма создания Информации
class InfoCreateForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['title']


# Форма создания Компонента
class ComponentCreateForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['c_type', 'material', 'thickness', 'band_count', 'remainder', 'pdf_draw', 'dxf_draw', 'part_file']


# Форма создания Проекта
class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['device']


# Форма создания Заказа
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['project', 'readiness']


# Форма создания Позиции
class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['order', 'component', 'quantity', 'priority', 'm_assembly', 'storage']


# Форма создания Позиции для заказа
class PositionCreateFormForOrder(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['component', 'quantity', 'priority', 'm_assembly', 'storage']


# Форма создания изготовителя
class ManufacturerCreateForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['title', 'n_email', 'contact_name', 'phone', 'city']


# Форма создания операции
class OperationCreateForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['title', 'manufacturer', 'priority']


# Форма создания Обеъединения позиции и операции
class AnAssociationCreateForm(forms.ModelForm):
    class Meta:
        model = AnAssociation
        fields = ['operation']
