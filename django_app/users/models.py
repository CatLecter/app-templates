from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(_('Дата создания пользователя'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления пользователя'), auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    full_name = models.CharField(_('Полное имя пользователя'), blank=False)
    phone = models.CharField(_('Телефон пользователя'), blank=False)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        db_table = '"public"."users"'

    def __str__(self):
        return str(self.uuid)
