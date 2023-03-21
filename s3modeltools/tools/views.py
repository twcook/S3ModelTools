from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from .models import Project, Modeler


class IndexView(TemplateView):
    template_name = "index.html"
    
class AboutView(TemplateView):
    template_name = "about.html"

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 15

class ProjectCreate(CreateView):
    model = Project
    fields = ['prj_name', 'prj_description', 'prj_public', 'prj_published', 'prj_lang', 'prj_seq']
    template_name = 'project_create.html'
    context_object_name = 'project'

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['prj_name', 'prj_description', 'prj_public', 'prj_published', 'prj_lang', 'prj_seq']
    template_name = 'project_update.html'
    context_object_name = 'project'    

class ModelerListView(ListView):
    model = Modeler
    template_name = 'modeler_list.html'
    context_object_name = 'modelers'
    paginate_by = 15

class ModelerCreate(CreateView):
    model = Modeler
    fields = ['mdl_name', 'mdl_description', 'mdl_public', 'mdl_published', 'mdl_lang', 'mdl_seq']
    template_name = 'modeler_create.html'
    context_object_name = 'modeler' 

class ModelerUpdate(UpdateView):
    model = Modeler
    fields = ['mdl_name', 'mdl_description', 'mdl_public', 'mdl_published', 'mdl_lang', 'mdl_seq']
    template_name = 'modeler_update.html'
    context_object_name = 'modeler'

