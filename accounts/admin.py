from django.contrib import admin

# Register your models here.
from accounts.models import EmailActivation, Profile


class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = EmailActivation


admin.site.register(EmailActivation, EmailActivationAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'phone', 'uuid', 'ssn', 'country', 'country_flag', 'slug', 'timestamp', 'updated')
    list_display_links = ('user',)
    list_filter = ('user', 'phone')
    search_fields = ('user',)

    ordering = ('-timestamp',)
    fieldsets = (
        ('Basic Information', {'description': "User Profile Information",
                               'fields': (('user',), 'uuid',)}),
        ('Complete Full Information',
         {'classes': ('collapse',), 'fields': ('phone', 'ssn', 'slug', 'country', 'country_flag')}),)