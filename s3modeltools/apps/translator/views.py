from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView, DeleteView

from translator.models import DMD, Record


class DMDListView(ListView):
    model = DMD
    context_object_name = 'dmds'
    template_name = 'translator/dmd_list.html'

class DMDUpdateView(UpdateView):
    model = DMD
    fields = '__all__'
    template_name = 'translator/dmd_form.html'
    success_url = '/dmd_list'

class DMDCreateView(CreateView):
    model = DMD
    fields = '__all__'
    template_name = 'translator/dmd_form.html'
    success_url = '/dmd_list'

class DMDDeleteView(DeleteView):
    model = DMD
    success_url = '/dmd_list'



class RecListView(ListView):
    model = Record
    context_object_name = 'recs'
    template_name = 'translator/rec_list.html'

class RecUpdateView(UpdateView):
    model = Record
    fields = '__all__'
    template_name = 'translator/rec_form.html'
    success_url = '/rec_list'

class RecCreateView(CreateView):
    model = Record
    fields = '__all__'
    template_name = 'translator/rec_form.html'
    success_url = '/rec_list'

class RecDeleteView(DeleteView):
    model = Record
    success_url = '/rec_list'
