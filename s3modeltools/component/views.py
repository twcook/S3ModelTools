from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from component.models import Attestation, Audit, Cluster, DM, Participation, Party, Predicate, PredObj, \
     ReferenceRange, SimpleReferenceRange, Units, XdBoolean, XdCount, XdLink, XdFile, XdFloat, XdString, \
     XdInterval, XdOrdinal, XdTemporal, XdQuantity

class AttestationList(ListView):
    model = Attestation
    template_name = 'attestation_list.html'
    context_object_name = 'attestations'
    paginate_by = 15

    
class AttestationCreate(CreateView):
    model = Attestation
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq', \
              'view', 'proof', 'reason', 'committer']
    template_name = 'attestation_create.html'
    context_object_name = 'attestation'

class AttestationUpdate(UpdateView):
    model = Attestation
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq', \
              'view', 'proof', 'reason', 'committer']
    template_name = 'attestation_update.html'
    context_object_name = 'attestation'


class AuditList(ListView):
    model = Audit
    template_name = 'audit_list.html'
    context_object_name = 'audits'
    paginate_by = 15

    
class AuditCreate(CreateView):
    model = Audit
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'audit_create.html'
    context_object_name = 'audit'


class AuditUpdate(UpdateView):
    model = Audit
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'audit_update.html'
    context_object_name = 'audit'


class BooleanList(ListView):
    model = XdBoolean
    template_name = 'boolean_list.html'
    context_object_name = 'booleans'
    paginate_by = 15

    
class BooleanCreate(CreateView):
    model = XdBoolean
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'boolean_create.html'
    context_object_name = 'boolean'


class BooleanUpdate(UpdateView):
    model = XdBoolean
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'boolean_update.html'
    context_object_name = 'boolean'


class ClusterList(ListView):
    model = Cluster
    template_name = 'cluster_list.html'
    context_object_name = 'clusters'
    paginate_by = 15

    
class ClusterCreate(CreateView):
    model = Cluster
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'cluster_create.html'
    context_object_name = 'cluster'


class ClusterUpdate(UpdateView):
    model = Cluster
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'cluster_update.html'
    context_object_name = 'cluster'


class CountList(ListView):
    model = XdCount
    template_name = 'count_list.html'
    context_object_name = 'counts'
    paginate_by = 15

    
class CountCreate(CreateView):
    model = XdCount
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'count_create.html'
    context_object_name = 'count'


class CountUpdate(UpdateView):
    model = XdCount
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'count_update.html'
    context_object_name = 'count'


class DataModelList(ListView):
    model = DM
    template_name = 'datamodel_list.html'
    context_object_name = 'datamodels'
    paginate_by = 15
    
class DataModelCreate(CreateView):
    model = DM
    fields = ['project', 'title', 'description', 'published']
    template_name = 'datamodel_create.html'
    context_object_name = 'datamodel'


class DataModelUpdate(UpdateView):
    model = DM
    fields = ['project', 'title', 'description', 'published']
    template_name = 'datamodel_update.html'
    context_object_name = 'datamodel'


class FileList(ListView):
    model = XdFile
    template_name = 'file_list.html'
    context_object_name = 'files'
    paginate_by = 15

    
class FileCreate(CreateView):
    model = XdFile
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'file_create.html'
    context_object_name = 'file'


class FileUpdate(UpdateView):
    model = XdFile
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'file_update.html'
    context_object_name = 'file'


class FloatList(ListView):
    model = XdFloat
    template_name = 'float_list.html'
    context_object_name = 'floats'
    paginate_by = 15

    
class FloatCreate(CreateView):
    model = XdFloat
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'float_create.html'
    context_object_name = 'float'


class FloatUpdate(UpdateView):
    model = XdFloat
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'float_update.html'
    context_object_name = 'float'


class IntervalList(ListView):
    model = XdInterval
    template_name = 'interval_list.html'
    context_object_name = 'intervals'
    paginate_by = 15

    
class IntervalCreate(CreateView):
    model = XdInterval
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'interval_create.html'
    context_object_name = 'interval'


class IntervalUpdate(UpdateView):
    model = XdInterval
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'interval_update.html'
    context_object_name = 'interval'


class LinkList(ListView):
    model = XdLink
    template_name = 'link_list.html'
    context_object_name = 'links'
    paginate_by = 15

    
class LinkCreate(CreateView):
    model = XdLink
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'link_create.html'
    context_object_name = 'link'


class LinkUpdate(UpdateView):
    model = XdLink
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'link_update.html'
    context_object_name = 'link'


class OrdinalList(ListView):
    model = XdOrdinal
    template_name = 'ordinal_list.html'
    context_object_name = 'ordinals'
    paginate_by = 15

    
class OrdinalCreate(CreateView):
    model = XdOrdinal
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'ordinal_create.html'
    context_object_name = 'ordinal'


class OrdinalUpdate(UpdateView):
    model = XdOrdinal
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'ordinal_update.html'
    context_object_name = 'ordinal'


class ParticipationList(ListView):
    model = Participation
    template_name = 'participation_list.html'
    context_object_name = 'participations'
    paginate_by = 15

    
class ParticipationCreate(CreateView):
    model = Participation
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'participation_create.html'
    context_object_name = 'participation'


class ParticipationUpdate(UpdateView):
    model = Participation
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'participation_update.html'
    context_object_name = 'participation'


class PartyList(ListView):
    model = Party
    template_name = 'party_list.html'
    context_object_name = 'parties'
    paginate_by = 15

    
class PartyCreate(CreateView):
    model = Party
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'party_create.html'
    context_object_name = 'party'


class PartyUpdate(UpdateView):
    model = Party
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'party_update.html'
    context_object_name = 'party'


class PredicateList(ListView):
    model = Predicate
    template_name = 'predicate_list.html'
    context_object_name = 'predicates'
    paginate_by = 15
    
class PredicateCreate(CreateView):
    model = Predicate
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'predicate_create.html'
    context_object_name = 'predicate'


class PredicateUpdate(UpdateView):
    model = Predicate
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'predicate_update.html'
    context_object_name = 'predicate'


class QuantityList(ListView):
    model = XdQuantity
    template_name = 'quantity_list.html'
    context_object_name = 'quantities'
    paginate_by = 15

    
class QuantityCreate(CreateView):
    model = XdQuantity
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'quantity_create.html'
    context_object_name = 'quantity'


class QuantityUpdate(UpdateView):
    model = XdQuantity
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'quantity_update.html'
    context_object_name = 'quantity'


class RDFObjectList(ListView):
    model = PredObj
    template_name = 'rdfobject_list.html'
    context_object_name = 'rdfobjects'
    paginate_by = 15

    
class RDFObjectCreate(CreateView):
    model = PredObj
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'rdfobject_create.html'
    context_object_name = 'rdfobject'


class RDFObjectUpdate(UpdateView):
    model = PredObj
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'rdfobject_update.html'
    context_object_name = 'rdfobject'


class ReferenceRangeList(ListView):
    model = ReferenceRange
    template_name = 'referencerange_list.html'
    context_object_name = 'referenceranges'
    paginate_by = 15

    
class ReferenceRangeCreate(CreateView):
    model = ReferenceRange
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'referencerange_create.html'
    context_object_name = 'referencerange'


class ReferenceRangeUpdate(UpdateView):
    model = ReferenceRange
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'referencerange_update.html'
    context_object_name = 'referencerange'


class SimpleReferenceRangeList(ListView):
    model = SimpleReferenceRange
    template_name = 'simplereferencerange_list.html'
    context_object_name = 'simplereferenceranges'
    paginate_by = 15

    
class SimpleReferenceRangeCreate(CreateView):
    model = SimpleReferenceRange
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'simplereferencerange_create.html'
    context_object_name = 'simplereferencerange'


class SimpleReferenceRangeUpdate(UpdateView):
    model = SimpleReferenceRange
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'simplereferencerange_update.html'
    context_object_name = 'simplereferencerange'


class StringList(ListView):
    model = XdString
    template_name = 'string_list.html'
    context_object_name = 'strings'
    paginate_by = 15

    
class StringCreate(CreateView):
    model = XdString
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'string_create.html'
    context_object_name = 'string'


class StringUpdate(UpdateView):
    model = XdString
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'string_update.html'
    context_object_name = 'string'


class TemporalList(ListView):
    model = XdTemporal
    template_name = 'temporal_list.html'
    context_object_name = 'temporals'
    paginate_by = 15

    
class TemporalCreate(CreateView):
    model = XdTemporal
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'temporal_create.html'
    context_object_name = 'temporal'


class TemporalUpdate(UpdateView):
    model = XdTemporal
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'temporal_update.html'
    context_object_name = 'temporal'


class UnitsList(ListView):
    model = Units
    template_name = 'units_list.html'
    context_object_name = 'units'
    paginate_by = 15

    
class UnitsCreate(CreateView):
    model = Units
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'units_create.html'
    context_object_name = 'units'


class UnitsUpdate(UpdateView):
    model = Units
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'units_update.html'
    context_object_name = 'units'

