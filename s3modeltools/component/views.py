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


class DMList(ListView):
    model = DM
    template_name = 'datamodel_list.html'
    context_object_name = 'datamodels'
    paginate_by = 15

    
class DMCreate(CreateView):
    model = DM
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'datamodel_create.html'
    context_object_name = 'datamodel'


class DMUpdate(UpdateView):
    model = DM
    fields = ['project', 'label', 'description', 'public', 'published', 'lang', 'pred_obj', 'seq']
    template_name = 'datamodel_update.html'
    context_object_name = 'datamodel'


