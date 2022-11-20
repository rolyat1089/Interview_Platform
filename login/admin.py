from django.contrib import admin
from login.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AcconutAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_candidate', 'last_login', 'is_admin', 'is_assessor', 'ApplicationNo')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AcconutAdmin)
