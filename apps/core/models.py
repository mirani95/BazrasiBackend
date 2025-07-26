from django.db import models
from django.conf import settings
from crum import get_current_user


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_createddby",
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_modifiedby",
        null=True,
        blank=True,
    )
    creator_info = models.CharField(max_length=100, null=True)
    modifier_info = models.CharField(max_length=100, null=True)
    trash = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()  # get user object
        self.modified_by = user
        if not self.creator_info:
            self.created_by = user
            self.creator_info = user.first_name + ' ' + user.last_name
        self.modifier_info = user.first_name + ' ' + user.last_name
        super(BaseModel, self).save(*args, **kwargs)
