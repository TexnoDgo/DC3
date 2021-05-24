from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Таблица Информация
class Info(models.Model):
    P_TYPE_VAR = (
        ('DEVICE', 'DEVICE'),
        ('PROJECT', 'PROJECT'),
        ('ORDER', 'ORDER'),
        ('COMPONENT', 'COMPONENT')
    )
    title = models.CharField(max_length=255, unique=True, verbose_name='НАИМЕНОВАНИЕ')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(default=timezone.now)
    p_class = models.CharField(max_length=20, choices=P_TYPE_VAR)

    def __str__(self):
        return self.title + '-' + self.p_class


# Таблица Устройств
class Device(models.Model):
    info = models.OneToOneField(Info, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return self.info.title


# Таблица Проектов
class Project(models.Model):
    info = models.OneToOneField(Info, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, verbose_name='УСТРОЙСТВО')

    def __str__(self):
        return self.info.title


# Таблица Заказов
class Order(models.Model):
    info = models.OneToOneField(Info, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='ПРОЕКТ')
    readiness = models.DateField(verbose_name='ДАТА ГОТОВНОСТИ')
    table = models.FileField(upload_to="ORDER_TABLE", default=None)
    position_qr_code_list = models.FileField(upload_to="POSITION_QR_CODE_LIST", default=None)

    def __str__(self):
        return self.info.title


# Таблица Компонентов
class Component(models.Model):
    COMPONENT_TYPE = (
        ('PART', 'PART'),
        ('ASSEMBLY', 'ASSEMBLY')
    )
    info = models.OneToOneField(Info, on_delete=models.CASCADE)
    pdf_draw = models.FileField(upload_to="COMPONENT_PDF_DRAW", null=True, blank=True,
                                verbose_name='ЧЕРТЕЖ PDF')
    png_draw = models.FileField(upload_to="COMPONENT_PNG_DRAW", null=True, blank=True,
                                verbose_name='ЧЕРТЕЖ PNG')
    c_type = models.CharField(choices=COMPONENT_TYPE, default='PART', max_length=20,
                              verbose_name='ТИП')
    material = models.CharField(max_length=150, default='default', verbose_name='МАТЕРИАЛ')
    thickness = models.CharField(max_length=10, default='0', verbose_name='ТОЛЩИНА')
    band_count = models.CharField(max_length=10, default='0', verbose_name='КОЛ-ВО ГИБОВ')
    dxf_draw = models.FileField(upload_to='COMPONENT_DXF_FILE', null=True, blank=True,
                                verbose_name='ФАЙЛ DXF')
    part_file = models.FileField(upload_to='COMPONENT_PART_FILE', null=True, blank=True,
                                 verbose_name='ФАЙЛ SOLIDWORKS')
    remainder = models.IntegerField(default=0,
                                    verbose_name='ОСТАТОК')

    def __str__(self):
        return self.info.title


# Таблица Место хранения
class StoragePlace(models.Model):
    title = models.CharField(max_length=255, unique=True)
    n_row = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Таблица Позиций
class Position(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='ЗАКАЗ')
    component = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='related_primary_manual_roats',
                                  verbose_name='КОМПОНЕНТ')
    quantity = models.IntegerField(default=0, verbose_name='КОЛИЧЕСТВО')
    priority = models.IntegerField(default=0, verbose_name='ПРИОРИТЕТ')
    m_assembly = models.ForeignKey(Component, on_delete=models.CASCADE, related_name='related_secondary_manual_roats',
                                   blank=True, null=True, verbose_name='МАТЕРИНСКАЯ СБОРКА')
    code = models.CharField(max_length=13, unique=True)
    pk_prod_qr_code = models.FileField(upload_to='PK_PROD_QR_CODE', default=None)
    smart_prod_qr_code = models.FileField(upload_to='SMART_PROD_QR_CODE', default=None)
    pdf_draw_wt_qr_code = models.FileField(upload_to='PDF_DRAW_WT_QR_CODE', default=None)
    storage = models.ForeignKey(StoragePlace, on_delete=models.CASCADE, verbose_name='МЕСТО ХРАНЕНИЯ')

    def __str__(self):
        return self.order.info.title + " - " + self.component.info.title


# Таблица Транзакция
class Transaction(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    act = models.BooleanField()
    create = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.act:
            return self.position + " + " + self.quantity
        else:
            return self.position + " - " + self.quantity


# Таблица Изготовитель
class Manufacturer(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='НАЗВАНИЕ')
    n_email = models.EmailField(verbose_name='EMAIL')
    contact_name = models.CharField(max_length=255, verbose_name='КОНТАКТНОЕ ЛИЦО')
    phone = models.CharField(max_length=30, verbose_name='НОМЕР')
    city = models.CharField(max_length=50, verbose_name='ГОРОД')

    def __str__(self):
        return self.title


# Таблица Операции
class Operation(models.Model):
    title = models.CharField(max_length=255, unique=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# Таблица Объединение
class AnAssociation(models.Model):
    STATUS_TYPE = (
        ('NONE', 'NONE'),
        ('CREATE', 'CREATE'),
        ('WORK', 'WORK'),
        ('DONE', 'DONE'),
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, verbose_name='ОПЕРАЦИЯ')
    status = models.CharField(max_length=20, choices=STATUS_TYPE)

    def __str__(self):
        return self.position.component.info.title + " - " + self.operation.title


# Таблица Профиль
class Profile(models.Model):
    ROOT_STATUS_LIST = (
        ('DESIGNER', 'DESIGNER'),
        ('PRODUCTION', 'PRODUCTION'),
        ('GUEST', 'GUEST')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    root_status = models.CharField(max_length=100, choices=ROOT_STATUS_LIST, default='GUEST')
    active_project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    active_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, default='+38(099) 099-99-99')
    new_email = models.CharField(max_length=100, default='new_net@gmail.com')
    profile_user_name = models.CharField(max_length=20, default='Name')
    profile_user_last = models.CharField(max_length=20, default='Surname')

    def __str__(self):
        return "Profile: " + self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()