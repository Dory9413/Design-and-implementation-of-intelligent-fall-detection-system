from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from watch.models import User, Contact, Config, AcceleratorData, WatchCode, HeartRateData, GPSData
from import_export.admin import ExportActionMixin


class AccDataAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'event', 'x', 'y', 'z', 'situation')


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'watch_code')
    fieldsets = (
        (None, {'fields': (
        'username', 'firstname', 'lastname', 'phone', 'email', 'birthday', 'gender', 'watch_code')}),
    )

    # add_fieldsets = (None,
    #                  {
    #                      'classes': 'wide',
    #                      'fields': ('firstname', 'lastname', 'phone', 'email', 'birthday', 'gender', 'username', 'watch_code', 'password')
    #                  })

    # readonly_fields = ('created_at', 'updated_at',)

    def has_add_permission(self, request):
        return False


admin.site.register(User, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(Config)
admin.site.register(AcceleratorData, AccDataAdmin)
admin.site.register(WatchCode)
admin.site.register(HeartRateData)
admin.site.register(GPSData)