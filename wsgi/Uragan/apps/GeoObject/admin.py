from reversion import VersionAdmin
from suit.widgets import AutosizedTextarea

from django.contrib import admin
from django.forms import ModelForm

from .models import GeoObject, Images, SurveillancePlan
from apps.common.widgets import ColorPickerWidget

class GeoObjectAdminForm(ModelForm):
    class Meta:
        widgets = {
            'title': AutosizedTextarea,
            'short_description': AutosizedTextarea,
            'description': AutosizedTextarea,
            'color': ColorPickerWidget,
        }


class GeoObjectAdmin(VersionAdmin):
    form = GeoObjectAdminForm
    list_display = ('title', 'lat', 'lon', 'short_description',)

class ImagesAdmin(VersionAdmin):
    pass

class SurveillancePlanAdmin(VersionAdmin):
    pass


admin.site.register(GeoObject, GeoObjectAdmin)
admin.site.register(SurveillancePlan, ImagesAdmin)
admin.site.register(Images, SurveillancePlanAdmin)