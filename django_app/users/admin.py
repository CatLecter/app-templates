from django.contrib import admin
from users.models import User


class PersonsInlineAdmin(admin.TabularInline):
    model = User
    extra = 0
    verbose_name = 'Пользователи'
    autocomplete_fields = ('uuid',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone',
    )
    search_fields = (
        'full_name',
        'phone',
    )
    fields = (
        'full_name',
        'phone',
    )
    ordering = ('full_name',)
