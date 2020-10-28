import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Dashboard(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Dashboard Name"), max_length=250, blank=True)
    dashboard_id = models.CharField(_("Dashboard ID"), max_length=250, unique=True)
    thumbnail_url = models.CharField(_("Thumbnail URL"), max_length=250)
    license_type = models.ForeignKey(
        "accounts.License", verbose_name=_("License Type"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("dashboard")
        verbose_name_plural = _("dashboards")

    def __str__(self):
        return self.title