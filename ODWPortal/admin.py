from django.contrib import admin

from ODWPortal.models import Site, SiteSetup, Language, SiteAlternateSearches
# Register your models here.


admin.site.register(Site)


class SiteSetupAdmin(admin.ModelAdmin):
    list_display = ['site', 'afield', 'truncate_value']
admin.site.register(SiteSetup, SiteSetupAdmin)


class LanguageAdmin(admin.ModelAdmin):
    list_display = ['site_language', 'afield', 'truncate_value']
admin.site.register(Language, LanguageAdmin)


class SiteAlternateSearchesAdmin(admin.ModelAdmin):
    list_display = ['site', 'alt_site_id', 'alt_site_label']
admin.site.register(SiteAlternateSearches, SiteAlternateSearchesAdmin)