import os
import csv

from time import time
from django.contrib import messages
from s3mtools.settings import MEDIA_ROOT

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.shortcuts import get_object_or_404

from dmgen.models import XdString, XdCount, XdQuantity, XdFloat, XdTemporal, Cluster, DM, PredObj, Predicate, Party, Units, get_cuid
from dmgen.generator import generateDM
from dmgen.admin import generate_dm

from .models import DMD, Record
from .datagen import dataGen
from .rdfgen import rdfGen

def analyze_csv(modeladmin, request, queryset):
    """
    Add the headers to the Record table for editing.
    """
    for obj in queryset:
        msg = (obj.__str__() + " has been analyzed. Edit the eXtended Datatypes to improve the accuracy and quality. Then return here to Generate the model.", messages.SUCCESS)

        with open(os.path.join(MEDIA_ROOT, obj.csv_file.url)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=obj.delim)
            for hdr in reader.fieldnames:
                hdr = hdr.strip()

                rec = Record(dmd=obj, header=hdr, label=hdr, dt_type='xdstring', description='Created by the Data Insights, Inc. Data Translator.')
                rec.save()

        modeladmin.message_user(request, msg[0], msg[1])
analyze_csv.short_description = _("Analyze CSV")


def dmgen(modeladmin, request, queryset):
    """
    Generate a complete Data Model for this DMD.
    """

    columns = []

    for obj in queryset:
        # check for existing DM title
        title = DM.objects.filter(title=obj.title)
        if title:
            msg = (obj.__str__() + " -- Data Model title already exists. You can delete it from the Generator DM section or edit your title.", messages.ERROR)
            modeladmin.message_user(request, msg[0], msg[1])
            return

        msg = (obj.__str__() + " has been processed.", messages.SUCCESS)

        with open(os.path.join(MEDIA_ROOT, obj.csv_file.url)) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=obj.delim)
            for hdr in reader.fieldnames:
                if hdr in columns:
                    msg = (obj.__str__() + " Duplicate column names are not allowed.", messages.ERROR)
                    return
                else:
                    columns.append(hdr.strip())


        pred = get_object_or_404(Predicate, id=1)

        dmd_po, x = PredObj.objects.get_or_create(po_name='Definition for ' + obj.title, predicate=pred, object_uri=obj.definitions.splitlines()[0], project=obj.project)

        newsub = False
        subject, newsub = Party.objects.get_or_create(project=obj.project, label=obj.title + ' - DM Subject', lang=obj.lang, description=obj.description)
        if newsub:
            subject.pred_obj.add(dmd_po)
            subject.save()
            subject.publish(request)

        newprv = False
        provider, newprv = Party.objects.get_or_create(project=obj.project, label=obj.title + ' - DM Provider', lang=obj.lang, description=obj.description, ct_id=get_cuid())
        if newprv:
            provider.pred_obj.add(dmd_po)
            provider.save()
            provider.publish(request)

        cluster, x = Cluster.objects.get_or_create(project=obj.project, label=obj.title + ' - Cluster', lang=obj.lang, description=obj.description, ct_id=get_cuid())
        if x:
            cluster.pred_obj.add(dmd_po)
            cluster.save()

        dm = DM.objects.create(project=obj.project, title=obj.title, dc_language=obj.lang, description=obj.description, author=obj.author,  creator=obj.author, edited_by=obj.author, ct_id=get_cuid())
        dm.pred_obj.add(dmd_po)
        dm.save()
        lang = obj.lang

        recs = Record.objects.filter(dmd=obj)

        for col in columns:
            mc = None
            new = False
            rec = recs.get(header=col)
            if rec.dt_type == 'xdstring':
                mc = XdString.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_length=rec.min_length, max_length=rec.max_length, exact_length=rec.exact_length, enums=rec.enums, def_val=rec.def_val, adapter_ctid=get_cuid())

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdstring.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdcount':
                u, new = Units.objects.get_or_create(project=dm.project, label=rec.units_name, lang=lang, description='Units for ' + rec.label + '. ' + rec.description, enums=rec.units_name, definitions=rec.units_uri, adapter_ctid=get_cuid())
                if new:
                    rdf = PredObj.objects.create(po_name='Definition for ' + u.label, predicate=pred, object_uri=rec.units_uri, project=dm.project)
                    u.pred_obj.add(rdf)
                    u.save()
                if u.published is False:
                    u.publish(request)
                mc = XdCount.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_inclusive=rec.min_inclusive, max_inclusive=rec.max_inclusive, min_exclusive=rec.min_exclusive, max_exclusive=rec.max_exclusive, total_digits=rec.total_digits, units=u, adapter_ctid=get_cuid())

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdcount.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdfloat':
                u, new = Units.objects.get_or_create(project=dm.project, label=rec.units_name, lang=lang, description='Units for ' + rec.label + '. ' + rec.description, enums=rec.units_name, definitions=rec.units_uri, adapter_ctid=get_cuid())
                if new:
                    rdf = PredObj.objects.create(po_name='Definition for ' + u.label, predicate=pred, object_uri=rec.units_uri, project=dm.project)
                    u.pred_obj.add(rdf)
                    u.save()
                if u.published is False:
                    u.publish(request)

                mc = XdFloat.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_inclusive=rec.min_inclusive, max_inclusive=rec.max_inclusive, min_exclusive=rec.min_exclusive, max_exclusive=rec.max_exclusive, total_digits=rec.total_digits, units=u, adapter_ctid=get_cuid())

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdfloat.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdquantity':
                u, new = Units.objects.get_or_create(project=dm.project, label=rec.units_name, lang=lang, description='Units for ' + rec.label + '. ' + rec.description, enums=rec.units_name, definitions=rec.units_uri, adapter_ctid=get_cuid())
                if new:
                    rdf = PredObj.objects.create(po_name='Definition for ' + u.label, predicate=pred, object_uri=rec.units_uri, project=dm.project)
                    u.pred_obj.add(rdf)
                    u.save()
                if u.published is False:
                    u.publish(request)

                mc = XdQuantity.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, min_inclusive=rec.min_inclusive, max_inclusive=rec.max_inclusive, min_exclusive=rec.min_exclusive, max_exclusive=rec.max_exclusive, total_digits=rec.total_digits, units=u, adapter_ctid=get_cuid())

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdquantity.add(mc)
                cluster.save()

            elif rec.dt_type == 'xdtemporal':
                mc = XdTemporal.objects.create(project=dm.project, label=rec.label, lang=lang, description=rec.description, allow_duration=rec.allow_duration, allow_date=rec.allow_date,
                                               allow_time=rec.allow_time, allow_datetime=rec.allow_datetime, allow_day=rec.allow_day, allow_month=rec.allow_month, allow_year=rec.allow_year,
                                               allow_year_month=rec.allow_year_month, allow_month_day=rec.allow_month_day, adapter_ctid=get_cuid())

                defs = rec.definitions.splitlines()
                if len(defs) <= 0:
                    mc.pred_obj.add(dmd_po)
                else:
                    for d in defs:
                        rdf = PredObj.objects.create(po_name='Definition for ' + mc.label, predicate=pred, object_uri=d, project=obj.project)
                        mc.pred_obj.add(rdf)
                        mc.save()

                msg = mc.publish(request)
                cluster.xdtemporal.add(mc)
                cluster.save()

            else:
                modeladmin.message_user(request, "Something broke while finding your datatype!", messages.ERROR)

        msg = cluster.publish(request)

        # need to send a queryset to the call to generate_dm from the dmgen admin
        qs = DM.objects.filter(ct_id=dm.ct_id)
        generate_dm(modeladmin, request, qs)

        if obj.data_gen:
            modeladmin.message_user(request, "Generating data files..........", messages.SUCCESS)
            dataGen(obj, dm)
            if obj.rdf_gen:
                modeladmin.message_user(request, "Generating RDF files..........", messages.SUCCESS)
                rdfGen(obj, dm)
        else:
            modeladmin.message_user(request, "Data and RDF Generation was skipped.", messages.WARNING)


        modeladmin.message_user(request, msg[0], msg[1])
dmgen.short_description = _("Generate a Data Model")

class RecordInline(admin.StackedInline):
    model = Record
    readonly_fields = ['header',]
    fieldsets = (
        ("Column", {'classes': ('wide',),
                'fields': (('header'),)}),
        ("General", {'classes': ('collapse',),
                                     'fields': ('label', 'description', 'dt_type', 'definitions',)}),
        ("Text", {'classes': ('collapse',),
                'fields': ('min_length', 'max_length', 'exact_length', 'enums', 'def_val', 'regex')}),
        ("Numbers", {'classes': ('collapse',),
                'fields': ('min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive','total_digits', 'units_name', 'units_uri', ),
                'description': _('<b>If a units entry is not defined here then one must be selected when editing the Count/Quantity in the Generator.</b>')}),
        ("Date/Time", {'classes': ('collapse',),
                'fields': (('allow_date', 'allow_time', 'allow_datetime'), ('allow_day', 'allow_month', 'allow_year'),
                           ('allow_year_month', 'allow_month_day', 'allow_duration'),),
                'description': _('<b>Select the specific temporal type in this column. ONE and ONLY ONE!</b>')}),
    )


class DMDAdmin(admin.ModelAdmin):
    inlines = [RecordInline]
    list_filter = ['project', 'author']
    actions = ['delete_selected', analyze_csv, dmgen,]
    list_display = ('title', 'project',)

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (('title', 'project'),'description','definitions',('author', 'contrib'),)}),
        ("Metadata", {'classes': ('wide',),
                                     'fields': ('subject','source', 'rights', 'relation', 'coverage', 'publisher', )}),
        ("Options", {'classes': ('wide',),
                    'fields': ('delim', 'lang', 'default_tz', 'data_gen', 'rdf_gen', 'csv_file', )}),
        ("Sub-Models", {'classes': ('collapse',),
                    'fields': ('audit', 'attestation', 'links')}),
    )

admin.site.register(DMD, DMDAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_filter = ['dmd', 'dt_type']
    actions = ['delete_selected', ]
    readonly_fields = ['header', 'dmd',]
    list_display = ('header','label', 'dt_type','dmd', )

    fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (('dmd', 'header'),)}),
        ("General", {'classes': ('wide',),
                                     'fields': ('label', 'description', 'dt_type', 'definitions',)}),
        ("Text", {'classes': ('collapse',),
                'fields': ('min_length', 'max_length', 'exact_length', 'enums', 'def_val', 'regex')}),
        ("Numbers", {'classes': ('collapse',),
                'fields': ('min_inclusive', 'max_inclusive', 'min_exclusive', 'max_exclusive','total_digits', 'units_name', 'units_uri', ),
                'description': _('<b>If a units entry is not defined here then one must be selected when editing the Count/Quantity in the Generator.</b>')}),
        ("Date/Time", {'classes': ('collapse',),
                'fields': (('allow_date', 'allow_time', 'allow_datetime'), ('allow_day', 'allow_month', 'allow_year'),
                           ('allow_year_month', 'allow_month_day', 'allow_duration'),),
                'description': _('<b>Select the specific temporal type in this column. ONE and ONLY ONE!</b>')}),
    )
admin.site.register(Record, RecordAdmin)
