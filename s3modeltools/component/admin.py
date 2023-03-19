from django.contrib import admin

from .models import XdBoolean, XdLink, XdString, Units, XdFile, XdInterval, ReferenceRange, SemanticLink, Namespace, \
    SimpleReferenceRange, XdOrdinal, XdTemporal, XdCount, XdQuantity, XdFloat, Party, Participation, Audit, Attestation, Cluster, DM


class ComponentAdminSite(admin.AdminSite):
    site_header = 'Component administration'

admin_site = ComponentAdminSite(name='componentadmin')

admin.site.register(Namespace)
admin.site.register(SemanticLink)
admin.site.register(XdBoolean)
admin.site.register(XdLink)
admin.site.register(XdString)
admin.site.register(Units)
admin.site.register(XdFile)
admin.site.register(XdInterval)
admin.site.register(ReferenceRange)
admin.site.register(SimpleReferenceRange)
admin.site.register(XdOrdinal)
admin.site.register(XdTemporal)
admin.site.register(XdCount)
admin.site.register(XdQuantity)
admin.site.register(XdFloat)
admin.site.register(Party)
admin.site.register(Participation)
admin.site.register(Audit)
admin.site.register(Attestation)
admin.site.register(Cluster)
admin.site.register(DM)

