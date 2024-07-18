from django.contrib.auth.models import AbstractUser, Group,Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_role = models.CharField(_('role'), max_length=10, choices=(('user', '일반사용자'), ('admin', '관리자')), default='user')
    birth_date = models.DateField(_('birth date'), blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="customuser_set",  # 이 부분을 명시적으로 변경
        related_query_name="customuser",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="customuser_set",  # 이 부분을 명시적으로 변경
        related_query_name="customuser",
    )