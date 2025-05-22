"""
Django Admin definitions.
"""
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from dmgen.models import get_cuid

from dmgen.models import Attestation, Audit, Modeler, Predicate, PredObj, NS, Project, Participation, ReferenceRange, SimpleReferenceRange, \
     Party, XdBoolean, XdFile, XdInterval, XdLink, XdOrdinal, XdCount, XdQuantity, XdFloat, XdRatio, XdString, XdTemporal, Cluster, DM, Units

from dmgen.forms import ParticipationAdminForm, AttestationAdminForm, AuditAdminForm, SimpleRRAdminForm, ReferenceRangeAdminForm, PartyAdminForm, \
     ClusterAdminForm, XdTemporalAdminForm, XdRatioAdminForm, XdQuantityAdminForm, XdFloatAdminForm, XdOrdinalAdminForm, XdFileAdminForm, XdIntervalAdminForm, \
     XdCountAdminForm, XdStringAdminForm, UnitsAdminForm, XdLinkAdminForm, XdBooleanAdminForm, DMAdminForm, DMAdminSUForm

from dmgen.generator import generateDM

# disable Django's sitewide delete
admin.site.disable_action('delete_selected')
# now add our own that checks for creator

def delete_mcs(modeladmin, request, queryset):
    # get the current users modeler id
    cur_modeler = Modeler.objects.filter(user=request.user)
    if cur_modeler:
        for obj in queryset:
            if hasattr(obj, 'label'):
                name = obj.label
            elif hasattr(obj, 'title'):
                name = obj.title
            else:
                name = " this object."
            if obj.creator.id != cur_modeler[0].id and request.user.is_superuser is False:
                modeladmin.message_user(request, "Cannot delete the model component " + name + " because " + cur_modeler[
                    0].user.username + " is not the creator.", messages.ERROR)
            else:
                    obj.delete()
    else:
        modeladmin.message_user(request, request.user.username +
                                " is not a registered DMGen modeler. ", messages.ERROR)

delete_mcs.short_description = _("Delete MC(s)")


def make_published(modeladmin, request, queryset):
    for obj in queryset:
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
            continue
        if not obj.published:  # publish and save code
            msg = obj.publish(request)

        else:
            msg = (obj.__str__() + " is already Published.", messages.WARNING)

        modeladmin.message_user(request, msg[0], msg[1])
make_published.short_description = _("Publish")


def republish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            if obj.published is True:  # re-publish and save code
                obj.published = False
                obj.schema_code = ''
                obj.ct_id = get_cuid()
                try:
                    obj.adapter_ctid = get_cuid()
                except AttributeError:
                    pass
                obj.save()
                msg = obj.publish(request)
                modeladmin.message_user(request, msg[0], msg[1])
    else:
        msg = ("User: " + request.user.username +
               " is not authorized to unpublish items.", messages.ERROR)
        modeladmin.message_user(request, msg[0], msg[1])

republish.short_description = _("Re-Publish (Development Only!)")


def republish_all(modeladmin, request, queryset):
    if request.user.is_superuser:
        q = XdBoolean.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdBooleans.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")
        q = Units.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Units.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdString.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdStrings.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdLink.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdLinks.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdInterval.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdIntervals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = ReferenceRange.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " ReferenceRanges.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdOrdinal.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdOrdinals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdCount.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdCounts.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdQuantity.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdQuantities.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdRatio.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdRatios.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdFile.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdFiles.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = XdTemporal.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " XdTemporals.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")
            else:
                print(obj.__str__() + " was republished.")

        q = Cluster.objects.filter(published=True)
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.save()

        q2 = []
        q3 = []
        print("Re-publishing " + str(len(q)) + " Clusters.")
        print("Clusters pass #1")
        for obj in q:
            obj.publish(request)
            print(obj.label, obj.published)
            if obj.published is False:
                q2.append(obj)

        print("Clusters pass #2")
        print("Re-publishing " + str(len(q2)) + " Clusters.")
        for obj in q2:
            if obj.published is False:
                obj.publish(request)
                if obj.published is False:
                    q3.append(obj)

        print("Clusters pass #3")
        print("Re-publishing " + str(len(q3)) + " Clusters.")
        for obj in q3:
            if obj.published is False:
                obj.publish(request)
                if obj.published is False:
                    print("Could not publish: ", obj.__str__())

        q = Party.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Partys.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")

        q = Participation.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Participations.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")

        q = Attestation.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Attestations.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")

        q = Audit.objects.filter(published=True)
        print("Re-publishing " + str(len(q)) + " Audits.")
        for obj in q:
            obj.published = False
            obj.schema_code = ''
            obj.ct_id = get_cuid()
            obj.save()
            msg = obj.publish(request)
            if msg[1] != messages.SUCCESS:  # there was an error.
                print(obj.__str__() + " WAS NOT republished.")


        print("Finished!!!!!")
    else:
        msg = ("User: " + request.user.username +
               " is not authorized to Republish items.", messages.ERROR)

republish_all.short_description = _("Re-Publish ALL (Development Only!)")


def unpublish(modeladmin, request, queryset):
    if request.user.is_superuser:
        for obj in queryset:
            obj.schema_code = ''

            obj.published = False
            msg = (obj.__str__() + " was Unpublished!", messages.SUCCESS)
            obj.save()
    else:
        msg = ("User: " + request.user.username + " is not authorized to unpublish items.", messages.ERROR)

    modeladmin.message_user(request, msg[0], msg[1])

unpublish.short_description = _("UnPublish (Development Only!)")

def unpublish_all(modeladmin, request, queryset):
    if request.user.is_superuser:
        msg = ("Unpublish ALL (Development Only!)", messages.WARNING)
        modeladmin.message_user(request, msg[0], msg[1])
        q = XdBoolean.objects.all()
        print("Unpublishing " + str(len(q)) + " XdBooleans.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Units.objects.all()
        print("Unpublishing " + str(len(q)) + " Units.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdString.objects.all()
        print("Unpublishing " + str(len(q)) + " XdStrings.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdLink.objects.all()
        print("Unpublishing " + str(len(q)) + " XdLinks.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdInterval.objects.all()
        print("Unpublishing " + str(len(q)) + " XdIntervals.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = ReferenceRange.objects.all()
        print("Unpublishing " + str(len(q)) + " ReferenceRanges.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdOrdinal.objects.all()
        print("Unpublishing " + str(len(q)) + " XdOrdinals.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdCount.objects.all()
        print("Unpublishing " + str(len(q)) + " XdCounts.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdQuantity.objects.all()
        print("Unpublishing " + str(len(q)) + " XdQuantities.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdRatio.objects.all()
        print("Unpublishing " + str(len(q)) + " XdRatios.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdFile.objects.all()
        print("Unpublishing " + str(len(q)) + " XdFiles.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = XdTemporal.objects.all()
        print("Unpublishing " + str(len(q)) + " XdTemporals.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.adapter_ctid = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Cluster.objects.all()
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Party.objects.all()
        print("Unpublishing " + str(len(q)) + " Partys.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Participation.objects.all()
        print("Unpublishing " + str(len(q)) + " Participations.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Attestation.objects.all()
        print("Unpublishing " + str(len(q)) + " Attestations.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = Audit.objects.all()
        print("Unpublishing " + str(len(q)) + " Audits.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.save()

        q = DM.objects.all()
        print("Unpublishing " + str(len(q)) + " DMs.")
        for obj in q:
            obj.published = False
            obj.ct_id = get_cuid()
            obj.schema_code = ''
            obj.html_file.delete()
            obj.xml_file.delete()
            obj.json_file.delete()
            obj.xsd_file.delete()
            obj.sha1_file.delete()
            obj.zip_file.delete()
            obj.save()

        msg = ("Finished Unpublishing!!!!!", messages.SUCCESS)
    else:
        msg = ("User: " + request.user.username + " is not authorized to Republish items.", messages.ERROR)

    modeladmin.message_user(request, msg[0], msg[1])
    
unpublish_all.short_description = _("Unpublish ALL (Development Only!)")


def copy_dt(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = get_cuid()
        new_obj.adapter_ctid = get_cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_dt.short_description = _("Copy Datatype(s)")


def copy_labeled(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = get_cuid()
        new_obj.adapter_ctid = get_cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_labeled.short_description = _("Copy Item(s)")


def copy_cluster(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = get_cuid()
        new_obj.adapter_ctid = get_cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_cluster.short_description = _("Copy Cluster(s)")


def copy_entry(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = get_cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_entry.short_description = _("Copy Entries")


def copy_dm(modeladmin, request, queryset):
    cur_modeler = Modeler.objects.filter(user=request.user)
    for obj in queryset:
        new_obj = obj
        new_obj.creator = cur_modeler[0]
        new_obj.pk = None
        new_obj.title = obj.title + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = get_cuid()
        new_obj.identifier = 'dm-' + new_obj.ct_id
        new_obj.save()
        msg = (obj.__str__() + " was Created!", messages.SUCCESS)

        modeladmin.message_user(request, msg[0], msg[1])

copy_dm.short_description = _("Copy DM")


def generate_dm(modeladmin, request, queryset):

    if len(queryset) > 1:
        msg = (_("You may only publish one DM at a time. " + str(len(queryset)) + " were selected."), messages.ERROR)
    elif queryset[0].published and request.user.is_superuser is False:
        msg = (_("This DM has been previously published. Please make a copy and publish a new one."), messages.ERROR)
    else:
        obj = queryset[0]
        obj.identifier = 'dm-' + str(obj.ct_id)
        obj.save()
        modeladmin.message_user(request, "Publishing the dm-" + str(obj.ct_id) + " package." + obj.title, messages.INFO)
        msg = generateDM(obj, request)
        # final msg from generator says success. create a standard success msg.
        if msg[1] == messages.SUCCESS:
            msg = (obj.__str__() + " with ID: " + obj.identifier + " was published!", messages.SUCCESS)

    modeladmin.message_user(request, msg[0], msg[1])

generate_dm.short_description = _("Generate DM Package")


def copy_prj(modeladmin, request, queryset):
    for obj in queryset:
        new_obj = obj
        new_obj.pk = None
        new_obj.prj_name = (obj.prj_name + " (***COPY***)")
        new_obj.description = obj.description
        new_obj.rm_version = obj.rm_version
        new_obj.allowed_groups = obj.allowed_groups
        new_obj.save()
copy_prj.short_description = _("Copy Project(s)")


class DMAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    ordering = ['project', 'title']
    search_fields = ['title', 'ct_id']
    actions = [copy_dm, generate_dm, delete_mcs, republish_all, unpublish_all,]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['contrib', 'pred_obj', ]

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('title', 'project', 'published')}),
        ("Metadata ", {'classes': ('collapse',),
                       'fields': ('dc_language', 'about', 'description', 'author', 'contrib', 'dc_subject', 'source', 'rights', 'relation', 'coverage', 'publisher',),
                       'description': _("Enter the <a href='http://dublincore.org/'>Dublin Core</a> Metadata")}),        
        ("Semantics ", {'classes': ('collapse',),
                                     'fields': ('pred_obj', ),
                                     'description': _("External semantic links for this model.")}),
        ("Data Model Content", {'classes': ('wide',),
                      'fields': ('language', 'encoding', 'data', 'subject', 'provider', 'participations', 'protocol', 'workflow', 'audit', 'attestation', 'links', 'acs',),
                      'description': _('Primary content nodes.',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code', 'html_file', 'xml_file', 'xsd_file', 'json_file', 'sha1_file', 'zip_file',)}),
    )

    def get_form(self, request, obj=None, **kwargs):
        
        # This is kind of a bad idea. Everytime the superuser views the DM it unpublishes it. 
        # The process needs to be intentional
        
        #if request.user.is_superuser:
            #kwargs['form'] = DMAdminSUForm
        #else:
            #kwargs['form'] = DMAdminForm

        kwargs['form'] = DMAdminForm
        
        form = super(DMAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('title', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(DM, DMAdmin)


class XdBooleanAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator', ]
    search_fields = ['label', 'ct_id', ]
    ordering = ['project', 'label', ]
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = XdBooleanAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdBooleanAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'trues', 'falses')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdBoolean, XdBooleanAdmin)


class XdLinkAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = XdLinkAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdLinkAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'link', 'relation', 'relation_uri',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdLink, XdLinkAdmin)


class XdStringAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['pred_obj', ]
    form = XdStringAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdStringAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('min_length', 'max_length', 'exact_length', 'enums', 'definitions', 'def_val', 'str_fmt',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdString, XdStringAdmin)


class UnitsAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code',
                       'creator', 'edited_by', ]
    form = UnitsAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(UnitsAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'enums', 'definitions', 'def_val',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),

    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Units, UnitsAdmin)


class XdCountAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdCountAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdCountAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act',)}),
        ("Units", {'classes': ('wide',),
                   'fields': ('units',),
                   'description': _('<b>Mandatory:</b> Select a units.')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'require_ms', 'require_error', 'require_accuracy',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location', 'allow_ms', 'allow_error', 'allow_accuracy',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdCount, XdCountAdmin)


class XdIntervalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = XdIntervalAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdIntervalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'interval_type', 'lower', 'upper',
                           'lower_included', 'upper_included', 'lower_bounded', 'upper_bounded',)}),
        ("Optional Units", {'classes': ('collapse',),
                            'fields': ('units_name', 'units_uri',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdInterval, XdIntervalAdmin)


class XdFileAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = XdFileAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdFileAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', )}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj', 'content_mode', 'encoding','language',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('media_type', 'alt_txt',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdFile, XdFileAdmin)


class XdOrdinalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdOrdinalAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdOrdinalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'ordinals', 'symbols', 'annotations',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdOrdinal, XdOrdinalAdmin)


class XdQuantityAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdQuantityAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdQuantityAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', )}),
        ("Units", {'classes': ('wide',),
                   'fields': ('units',),
                   'description': _('<b>Mandatory:</b> Select a units.')}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',
                                 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'fraction_digits', 'require_ms', 'require_error', 'require_accuracy',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location', 'allow_ms', 'allow_error', 'allow_accuracy',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdQuantity, XdQuantityAdmin)


class XdFloatAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdFloatAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdFloatAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', )}),
        ("Units", {'classes': ('wide',),
                   'fields': ('units',),
                   'description': _('<b>Mandatory:</b> Select a units.')}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges', 'min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive', 'total_digits', 'require_ms', 'require_error', 'require_accuracy',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location', 'allow_ms', 'allow_error', 'allow_accuracy',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdFloat, XdFloatAdmin)


class XdRatioAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code',
                       'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdRatioAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdRatioAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', 'ratio_type',)}),
        ("Numerator Units (Optional and CANNOT be the same MC as the denominator or ratio.)", {'classes': ('collapse',),
                                                                                                'fields': ('num_units',),
                                                                                                'description': _('Select a units.')}),
        ("Denominator Units (Optional and CANNOT be the same MC as the numerator or ratio.)", {'classes': ('collapse',),
                                                                                                'fields': ('den_units',),
                                                                                                'description': _('Select a units.')}),
        ("Ratio Units (Optional and CANNOT be the same MC as the numerator or denominator.)", {'classes': ('collapse',),
                                                                                                'fields': ('ratio_units',),
                                                                                                'description': _('Select a units.')}),
        ("Optional Constraints", {'classes': ('collapse',),
                                  'fields': ('num_min_inclusive', 'num_max_inclusive', 'num_min_exclusive',
                                             'num_max_exclusive', 'den_min_inclusive', 'den_max_inclusive',
                                             'den_min_exclusive', 'den_max_exclusive', 'normal_status',
                                             'reference_ranges', 'min_magnitude', 'max_magnitude',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdRatio, XdRatioAdmin)


class XdTemporalAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['reference_ranges', 'pred_obj', ]
    form = XdTemporalAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(XdTemporalAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'require_vtb', 'require_vte', 'require_tr', 'require_mod', 'require_location', 'require_act', )}),
        ("Allow Only Duration Type", {'classes': ('wide',),
                                          'fields': ('allow_duration', )}),
        ("Allow Any Combination of these:", {'classes': ('wide',),
                                             'fields': ('allow_date', 'allow_time', 'allow_datetime', 'allow_day', 'allow_month',
                                                        'allow_year', 'allow_year_month', 'allow_month_day',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Optional", {'classes': ('collapse',),
                      'fields': ('normal_status', 'reference_ranges',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('ui_type', 'seq', 'validate', 'allow_vtb', 'allow_vte', 'allow_tr', 'allow_mod', 'allow_location')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(XdTemporal, XdTemporalAdmin)


class ClusterAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_cluster, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['xdboolean', 'xdlink', 'xdstring', 'clusters', 'xdfile',
                         'xdordinal', 'xdtemporal', 'xdcount', 'xdquantity', 'xdfloat', 'xdratio', 'pred_obj', ]
    form = ClusterAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClusterAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'public'), 'description', 'pred_obj',)}),
        ("Contents", {'classes': ('wide',),
                      'fields': ('clusters',),
                      'description': _('Select all Clusters that you wish to include in this Cluster.'), }),
        ("Non-Quantitative", {'classes': ('wide',),
                              'fields': ('xdboolean', 'xdlink', 'xdstring', 'xdfile', 'xdordinal', 'xdtemporal',),
                              'description': _('Select one or more non-quantitative datatype(s) for this Cluster.')}),
        ("Quantitative", {'classes': ('wide',),
                          'fields': ('xdcount', 'xdquantity', 'xdfloat', 'xdratio',),
                          'description': _('Select one or more quantitative datatype(s) for this Cluster.')}),

        ("User Interface", {'classes': ('wide',),
                       'fields': ('seq', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Cluster, ClusterAdmin)


class PartyAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_labeled, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    filter_horizontal = ['external_ref', 'pred_obj', ]
    form = PartyAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(PartyAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'details', 'external_ref',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('seq', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Party, PartyAdmin)


class ReferenceRangeAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = ReferenceRangeAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ReferenceRangeAdmin, self).get_form(
            request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'definition',
                           'interval', 'is_normal',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(ReferenceRange, ReferenceRangeAdmin)


class SimpleRRAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish, copy_dt, republish, delete_mcs,  ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = SimpleRRAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(SimpleRRAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        form.prj_filter = modeller.prj_filter

        return form

    fieldsets = (
        (None, {'classes': ('wide', ),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'definition', 'is_normal', 'interval_type',
                           'lower', 'upper', 'lower_included', 'upper_included', 'lower_bounded',
                           'upper_bounded', )}),

        ("Optional Units", {'classes': ('collapse', ),
                            'fields': ('units_name', 'units_uri', )}),

        ("Additional Information ", {'classes': ('wide', ),
                                     'fields': ('description', 'pred_obj', )}),
        ("Read Only", {'classes': ('collapse', ),
                       'fields': ('creator', 'edited_by', 'schema_code', )}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator', )
admin.site.register(SimpleReferenceRange, SimpleRRAdmin)


class AuditAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = AuditAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AuditAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', 'project', 'label', 'lang', 'public')}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        (None, {'classes': ('wide',),
                'fields': ('system_id', 'system_user', 'location',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('seq', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Audit, AuditAdmin)


class AttestationAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = AttestationAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttestationAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'view', 'reason', 'proof', 'committer',)}),
        ("Additional Information", {'classes': ('wide',),
                                    'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('seq', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Attestation, AttestationAdmin)


class ParticipationAdmin(admin.ModelAdmin):
    list_filter = ['published', 'project', 'creator']
    search_fields = ['label', 'ct_id']
    ordering = ['project', 'label']
    actions = [make_published, unpublish,
               copy_labeled, republish, delete_mcs, ]
    readonly_fields = ['published', 'schema_code', 'creator', 'edited_by', ]
    form = ParticipationAdminForm
    filter_horizontal = ['pred_obj', ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ParticipationAdmin, self).get_form(request, obj, **kwargs)
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        form.current_user = request.user
        form.default_prj = modeller.project
        return form

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('published', ('label', 'project', 'lang', 'public'), 'performer', 'function', 'mode',)}),
        ("Additional Information ", {'classes': ('wide',),
                                     'fields': ('description', 'pred_obj',)}),
        ("User Interface", {'classes': ('wide',),
                       'fields': ('seq', 'validate')}),
        ("Read Only", {'classes': ('collapse',),
                       'fields': ('creator', 'edited_by', 'schema_code',)}),
    )

    def save_model(self, request, obj, form, change):
        modeller = get_object_or_404(Modeler, user_id=request.user.id)
        if obj.creator.id == 1:
            obj.creator = modeller
        obj.edited_by = modeller
        obj.save()

    list_display = ('label', 'project', 'published', 'edited_by', 'creator',)
admin.site.register(Participation, ParticipationAdmin)


class ProjectAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('prj_name', 'description',)
admin.site.register(Project, ProjectAdmin)


class NSAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('abbrev', 'uri',)
admin.site.register(NS, NSAdmin)


class PredicateAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('ns_abbrev', 'class_name',)
admin.site.register(Predicate, PredicateAdmin)


class PredObjAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    ordering = ['project', 'object_uri']
    list_filter = ['project', ]
    list_display = ('project', 'predicate', 'object_uri',)
admin.site.register(PredObj, PredObjAdmin)


class ModelerAdmin(admin.ModelAdmin):
    actions = ['delete_selected', ]
    list_display = ('name', 'email', 'user', 'project',)
admin.site.register(Modeler, ModelerAdmin)
