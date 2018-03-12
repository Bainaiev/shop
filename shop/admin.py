from . import forms
from django.contrib import admin
from .models import Product, Contact, User
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

class PriceFilter(admin.SimpleListFilter):
    title = 'price'
    parameter_name = 'price_limit'

    def lookups(self, request, model_admin):
        return (
            ('<100', '<100'),
            ('100<x<300', '>100 and <300'),
            ('>300', '>300'),
        )

    def queryset(self, request, queryset):
        if self.value() == '<100':
            return queryset.filter(price__lte=100)
        if self.value() == '100<x<300':
            return queryset.filter(price__lte=300, price__gte=100) 
        if self.value() == '>300':
            return queryset.filter(price__gte=300)             

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    save_as_continue = True

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'sex', 'category')
    list_filter = ('sex', 'category', PriceFilter)
    list_per_page = 50
    ordering = ('title',)


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'address', 'phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'address', 'phone')
    list_filter = ('is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'address', 'phone')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)

# Register your models here.
