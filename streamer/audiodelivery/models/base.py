from django.db import models

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from crum import get_current_user

from uuid import uuid4


class TimeLogMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )

    edited_at = models.DateTimeField(
        _("Edited At"),
        auto_now=True
    )

class UserLogMixin(models.Model):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Created By"),
        null=True,
        blank=True,
        related_name="%(class)s_creator_related",
        on_delete=models.SET_NULL
    )

    edited_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_("Edited By"),
        null=True,
        blank=True,
        related_name="%(class)s_editor_related",
        on_delete=models.SET_NULL
    )

class LogMixin(TimeLogMixin, UserLogMixin):
    class Meta:
        abstract = True

class BaseModel(LogMixin):
    class Meta:
        abstract = True

    id = models.UUIDField(
        _("ID"),
        default=uuid4,
        primary_key=True,
        unique=True
    )
    
    def save(self, *args, **kwargs):
        user = get_current_user()

        if user is None or user.is_anonymous:
            user = None
        
        if self._state.adding:
            self.created_by = user
        
        self.edited_by = user
        
        super(BaseModel, self).save(*args, **kwargs)


