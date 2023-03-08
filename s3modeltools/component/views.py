from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from component.models import Attestation, Audit

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


