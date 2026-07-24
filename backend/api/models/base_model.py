from django.db import models
from django.conf import settings
import uuid

class BaseModel(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, verbose_name="ID")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    is_deleted = models.BooleanField(default=False, verbose_name="Is Deleted")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Deleted At")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Updated At")
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name="Created User"
    )

    class Meta:
        abstract = True
