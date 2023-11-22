from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from accounts.models import User
from dealscan.sites import unfold_admin_site

admin.site.unregister(Group)


@admin.register(Group, site=unfold_admin_site)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(User, site=unfold_admin_site)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    model = User  # type: ignore[assignment]
    list_display = ["email", "username", "get_customer_id", "date_joined", "is_subscribed", "is_staff"]
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("date_joined",)
    readonly_fields = ("date_joined", "last_login")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    def get_customer_id(self, obj):
        return obj.stripe_user.customer_id if obj.stripe_user else None
    get_customer_id.short_description = 'Customer ID'

    def is_subscribed(self, obj):
        return bool(obj.stripe_user.subscription_id) if obj.stripe_user else None
