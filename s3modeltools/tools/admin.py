from django.contrib import admin

from .models import Project, Modeler

class ToolsAdminSite(admin.AdminSite):
    site_header = 'Tools administration'

admin_site = ToolsAdminSite(name='toolsadmin')

admin.site.register(Project)
admin.site.register(Modeler)


