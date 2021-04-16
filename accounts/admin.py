from django.contrib import admin

from accounts.models import MyUser, UserBed, Bed


class MyUserAdmin(admin.ModelAdmin):
    """
    Custom Model admin for Region Distributor Model.
    """
    list_display = ("first_name", "email", "is_active", )


class BedsAdmin(admin.ModelAdmin):
    """
    Custom Model admin for Region Distributor Model.
    """
    list_display = ("bed_number", "bed_type", "is_active", )


class UserBedsAdmin(admin.ModelAdmin):
    """
    Custom Model admin for Region Distributor Model.
    """
    list_display = ("user", "bed", "is_active", )


# Register your models here.
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Bed, BedsAdmin)
admin.site.register(UserBed, UserBedsAdmin)
