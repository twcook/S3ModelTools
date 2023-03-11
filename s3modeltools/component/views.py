from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from component.models import Attestation, Audit, Cluster, DM, NS, Participation, Party, Predicate, PredObj, \
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
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'datamodel_create.html'
    context_object_name = 'datamodel'


class DataModelUpdate(UpdateView):
    model = DM
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
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

