from cuid import cuid

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView, DeleteView

from .forms import ContactForm, SignUpForm, ModelerForm, AttestationForm, AuditForm, ClusterForm, BooleanForm, CountForm, DMForm, FileForm, FloatForm, IntervalForm, LinkForm, \
     OrdinalForm, ParticipationForm, PartyForm, QuantityForm, RatioForm, ReferenceRangeForm, StringForm, TemporalForm, UnitsForm

from tools.models import DM, Attestation, Audit, XdBoolean, Cluster, XdCount, XdFile, XdFloat, XdInterval, XdLink, XdOrdinal, XdQuantity, XdRatio, XdString, XdTemporal, Units, \
     Participation, Party, ReferenceRange, Modeler

from s3mtools.settings import STATIC_ROOT
from tools.generator import generateDM


def sign_up(request):
    title = 'Sign Up Now'
    form = SignUpForm(request.POST or None)
    context = {
        "title": title,
        "form": form
    }
    if form.is_valid():
        #form.save()
        #print request.POST['email'] #not recommended
        instance = form.save(commit=False)

        full_name = form.cleaned_data.get("full_name")
        if not full_name:
            full_name = "New full name"
        instance.full_name = full_name
        # if not instance.full_name:
        # 	instance.full_name = "Justin"
        instance.save()
        context = {
            "title": "Thank you"
        }

    if request.user.is_authenticated() and request.user.is_staff:
        #print(SignUp.objects.all())
        # i = 1
        # for instance in SignUp.objects.all():
        # 	print(i)
        # 	print(instance.full_name)
        # 	i += 1

        queryset = SignUp.objects.all().order_by('-timestamp') #.filter(full_name__iexact="Justin")
        #print(SignUp.objects.all().order_by('-timestamp').filter(full_name__iexact="Justin").count())
        context = {
            "queryset": queryset
        }

    return render(request, "home.html", context)


def contact(request):
    title = 'Contact Us'
    title_align_center = True
    form = ContactForm(request.POST or None)
    if form.is_valid():
        # for key, value in form.cleaned_data.iteritems():
        # 	print key, value
        # 	#print form.cleaned_data.get(key)
        form_email = form.cleaned_data.get("email")
        form_message = form.cleaned_data.get("message")
        form_full_name = form.cleaned_data.get("full_name")
        # print email, message, full_name
        subject = 'Site contact form'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, 'youotheremail@email.com']
        contact_message = "%s: %s via %s"%(
            form_full_name,
            form_message,
            form_email)
        some_html_message = """
		<h1>hello</h1>
		"""
        send_mail(subject,
                  contact_message,
                  from_email,
                  to_email,
                  html_message=some_html_message,
                  fail_silently=True)

    context = {
        "form": form,
        "title": title,
        "title_align_center": title_align_center,
    }
    return render(request, "forms.html", context)


class IndexView(TemplateView):
    template_name = 'tools/index.html'
    # do this to use simple variables in the template addressing them as view.my_var
    sdir = STATIC_ROOT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['modeler'] = get_object_or_404(Modeler, user=self.request.user)
        return context

class ToolsView(TemplateView):
    template_name = 'tools/tools.html'
    sdir = STATIC_ROOT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['modeler'] = get_object_or_404(Modeler, user=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class DMListView(ListView):
    model = DM
    context_object_name = 'datamodels'
    template_name = 'tools/dm_list.html'

@method_decorator(login_required, name='dispatch')
class DMGenerateView(TemplateView):
    model = DM
    template_name = 'tools/dm_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(DM, id = kwargs['pk'])
        if "(***COPY***)" in obj.title:  # skip publishing a copy.
            msg = (obj.title + " --Cannot generate a copy until it is edited.", messages.ERROR)
            messages.add_message(request, msg[1], msg[0])
            return HttpResponseRedirect('/dm_list')
        else:
            msg = generateDM(obj, request)
            messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/dm_list')

@method_decorator(login_required, name='dispatch')
class DMCopyView(TemplateView):
    model = DM
    template_name = 'tools/dm_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(DM, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.title = obj.title + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.title + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/dm_list')

@method_decorator(login_required, name='dispatch')
class DMUpdateView(UpdateView):
    model = DM
    form_class = DMForm
    template_name = 'tools/dm_form.html'
    success_url = '/dm_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        form.instance.language = form.instance.dc_language
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(DMUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class DMCreateView(CreateView):
    model = DM
    form_class = DMForm
    template_name = 'tools/dm_form.html'
    success_url = '/dm_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        form.instance.language = form.instance.dc_language
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(DMUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class DMDeleteView(DeleteView):
    model = DM
    success_url = '/dm_list'

@method_decorator(login_required, name='dispatch')
class AttListView(ListView):
    model = Attestation
    context_object_name = 'attestations'
    template_name = 'tools/att_list.html'

@method_decorator(login_required, name='dispatch')
class AttPublishView(TemplateView):
    model = Attestation
    template_name = 'tools/att_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Attestation, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/att_list')

@method_decorator(login_required, name='dispatch')
class AttCopyView(TemplateView):
    model = Attestation
    template_name = 'tools/att_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Attestation, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/att_list')

@method_decorator(login_required, name='dispatch')
class AttUpdateView(UpdateView):
    model = Attestation
    form_class = AttestationForm
    context_object_name = 'att'
    template_name = 'tools/att_form.html'
    success_url = '/att_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(AttUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class AttCreateView(CreateView):
    model = Attestation
    form_class = AttestationForm
    context_object_name = 'att'
    template_name = 'tools/att_form.html'
    success_url = '/att_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(AttCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs

@method_decorator(login_required, name='dispatch')
class AttDeleteView(DeleteView):
    model = Attestation
    success_url = '/att_list'

@method_decorator(login_required, name='dispatch')
class AudListView(ListView):
    model = Audit
    context_object_name = 'audits'
    template_name = 'tools/aud_list.html'

@method_decorator(login_required, name='dispatch')
class AudPublishView(TemplateView):
    model = Audit
    template_name = 'tools/aud_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Audit, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/aud_list')

@method_decorator(login_required, name='dispatch')
class AudCopyView(TemplateView):
    model = Audit
    template_name = 'tools/aud_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Audit, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/aud_list')

@method_decorator(login_required, name='dispatch')
class AudUpdateView(UpdateView):
    model = Audit
    form_class = AuditForm
    template_name = 'tools/aud_form.html'
    success_url = '/aud_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(AudUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class AudCreateView(CreateView):
    model = Audit
    form_class = AuditForm
    template_name = 'tools/aud_form.html'
    success_url = '/aud_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(AudCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class AudDeleteView(DeleteView):
    model = Audit
    success_url = '/aud_list'

@method_decorator(login_required, name='dispatch')
class BoolListView(ListView):
    model = XdBoolean
    context_object_name = 'booleans'
    template_name = 'tools/bool_list.html'

@method_decorator(login_required, name='dispatch')
class BoolPublishView(TemplateView):
    model = XdBoolean
    template_name = 'tools/bool_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdBoolean, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/bool_list')

@method_decorator(login_required, name='dispatch')
class BoolCopyView(TemplateView):
    model = XdBoolean
    template_name = 'tools/bool_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdBoolean, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/bool_list')

@method_decorator(login_required, name='dispatch')
class BoolUpdateView(UpdateView):
    model = XdBoolean
    form_class = BooleanForm
    template_name = 'tools/bool_form.html'
    success_url = '/bool_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(BoolUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class BoolCreateView(CreateView):
    model = XdBoolean
    form_class = BooleanForm
    template_name = 'tools/bool_form.html'
    success_url = '/bool_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(BoolCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class BoolDeleteView(DeleteView):
    model = XdBoolean
    success_url = '/bool_list'

@method_decorator(login_required, name='dispatch')
class CluListView(ListView):
    model = Cluster
    context_object_name = 'clusters'
    template_name = 'tools/clu_list.html'

@method_decorator(login_required, name='dispatch')
class CluPublishView(TemplateView):
    model = Cluster
    template_name = 'tools/clu_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Cluster, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/clu_list')

@method_decorator(login_required, name='dispatch')
class CluCopyView(TemplateView):
    model = Cluster
    template_name = 'tools/clu_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Cluster, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/clu_list')

@method_decorator(login_required, name='dispatch')
class CluUpdateView(UpdateView):
    model = Cluster
    form_class = ClusterForm
    template_name = 'tools/clu_form.html'
    success_url = '/clu_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CluUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class CluCreateView(CreateView):
    model = Cluster
    form_class = ClusterForm
    template_name = 'tools/clu_form.html'
    success_url = '/clu_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CluCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class CluDeleteView(DeleteView):
    model = Cluster
    success_url = '/clu_list'


@method_decorator(login_required, name='dispatch')
class CntListView(ListView):
    model = XdCount
    context_object_name = 'counts'
    template_name = 'tools/cnt_list.html'

@method_decorator(login_required, name='dispatch')
class CntPublishView(TemplateView):
    model = XdCount
    template_name = 'tools/cnt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdCount, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/cnt_list')

@method_decorator(login_required, name='dispatch')
class CntCopyView(TemplateView):
    model = XdCount
    template_name = 'tools/cnt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdCount, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/cnt_list')

@method_decorator(login_required, name='dispatch')
class CntUpdateView(UpdateView):
    model = XdCount
    form_class = CountForm
    template_name = 'tools/cnt_form.html'
    success_url = '/cnt_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CntUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class CntCreateView(CreateView):
    model = XdCount
    form_class = CountForm
    template_name = 'tools/cnt_form.html'
    success_url = '/cnt_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CntCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class CntDeleteView(DeleteView):
    model = XdCount
    success_url = '/cnt_list'

@method_decorator(login_required, name='dispatch')
class FilListView(ListView):
    model = XdFile
    context_object_name = 'files'
    template_name = 'tools/fil_list.html'

@method_decorator(login_required, name='dispatch')
class FilPublishView(TemplateView):
    model = XdFile
    template_name = 'tools/fil_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdFile, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/fil_list')

@method_decorator(login_required, name='dispatch')
class FilCopyView(TemplateView):
    model = XdFile
    template_name = 'tools/fil_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdFile, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/fil_list')

@method_decorator(login_required, name='dispatch')
class FilUpdateView(UpdateView):
    model = XdFile
    form_class = FileForm
    template_name = 'tools/fil_form.html'
    success_url = '/fil_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(FilUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class FilCreateView(CreateView):
    model = XdFile
    form_class = FileForm
    template_name = 'tools/fil_form.html'
    success_url = '/fil_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(FilCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class FilDeleteView(DeleteView):
    model = XdFile
    success_url = '/fil_list'

@method_decorator(login_required, name='dispatch')
class FltListView(ListView):
    model = XdFloat
    context_object_name = 'floats'
    template_name = 'tools/flt_list.html'

@method_decorator(login_required, name='dispatch')
class FltPublishView(TemplateView):
    model = XdFloat
    template_name = 'tools/flt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdFloat, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/flt_list')

@method_decorator(login_required, name='dispatch')
class FltCopyView(TemplateView):
    model = XdFloat
    template_name = 'tools/flt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdFloat, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/flt_list')

@method_decorator(login_required, name='dispatch')
class FltUpdateView(UpdateView):
    model = XdFloat
    form_class = FloatForm
    template_name = 'tools/flt_form.html'
    success_url = '/flt_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(FltUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class FltCreateView(CreateView):
    model = XdFloat
    form_class = FloatForm
    template_name = 'tools/flt_form.html'
    success_url = '/flt_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(FltCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class FltDeleteView(DeleteView):
    model = XdFloat
    success_url = '/flt_list'

@method_decorator(login_required, name='dispatch')
class IntListView(ListView):
    model = XdInterval
    context_object_name = 'intervals'
    template_name = 'tools/int_list.html'

@method_decorator(login_required, name='dispatch')
class IntPublishView(TemplateView):
    model = XdInterval
    template_name = 'tools/int_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdInterval, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/int_list')

@method_decorator(login_required, name='dispatch')
class IntCopyView(TemplateView):
    model = XdInterval
    template_name = 'tools/int_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdInterval, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/int_list')

@method_decorator(login_required, name='dispatch')
class IntUpdateView(UpdateView):
    model = XdInterval
    form_class = IntervalForm
    template_name = 'tools/int_form.html'
    success_url = '/int_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(IntUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class IntCreateView(CreateView):
    model = XdInterval
    form_class = IntervalForm
    template_name = 'tools/int_form.html'
    success_url = '/int_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(IntCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class IntDeleteView(DeleteView):
    model = XdInterval
    success_url = '/int_list'

@method_decorator(login_required, name='dispatch')
class LnkListView(ListView):
    model = XdLink
    context_object_name = 'links'
    template_name = 'tools/lnk_list.html'

@method_decorator(login_required, name='dispatch')
class LnkPublishView(TemplateView):
    model = XdLink
    template_name = 'tools/lnk_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdLink, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/lnk_list')

@method_decorator(login_required, name='dispatch')
class LnkCopyView(TemplateView):
    model = XdLink
    template_name = 'tools/lnk_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdLink, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/lnk_list')

@method_decorator(login_required, name='dispatch')
class LnkUpdateView(UpdateView):
    model = XdLink
    form_class = LinkForm
    template_name = 'tools/lnk_form.html'
    success_url = '/lnk_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(LnkUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class LnkCreateView(CreateView):
    model = XdLink
    form_class = LinkForm
    template_name = 'tools/lnk_form.html'
    success_url = '/lnk_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(LnkCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class LnkDeleteView(DeleteView):
    model = XdLink
    success_url = '/lnk_list'

@method_decorator(login_required, name='dispatch')
class OrdListView(ListView):
    model = XdOrdinal
    context_object_name = 'ordinals'
    template_name = 'tools/ord_list.html'

@method_decorator(login_required, name='dispatch')
class OrdPublishView(TemplateView):
    model = XdOrdinal
    template_name = 'tools/ord_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdOrdinal, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/ord_list')

@method_decorator(login_required, name='dispatch')
class OrdCopyView(TemplateView):
    model = XdOrdinal
    template_name = 'tools/ord_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdOrdinal, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/ord_list')

@method_decorator(login_required, name='dispatch')
class OrdUpdateView(UpdateView):
    model = XdOrdinal
    form_class = OrdinalForm
    template_name = 'tools/ord_form.html'
    success_url = '/ord_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(OrdUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class OrdCreateView(CreateView):
    model = XdOrdinal
    form_class = OrdinalForm
    template_name = 'tools/ord_form.html'
    success_url = '/ord_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(OrdCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class OrdDeleteView(DeleteView):
    model = XdOrdinal
    success_url = '/ord_list'

@method_decorator(login_required, name='dispatch')
class PtnListView(ListView):
    model = Participation
    context_object_name = 'participations'
    template_name = 'tools/ptn_list.html'

@method_decorator(login_required, name='dispatch')
class PtnPublishView(TemplateView):
    model = Participation
    template_name = 'tools/ptn_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Participation, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/ptn_list')

@method_decorator(login_required, name='dispatch')
class PtnCopyView(TemplateView):
    model = Participation
    template_name = 'tools/ptn_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Participation, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/ptn_list')

@method_decorator(login_required, name='dispatch')
class PtnUpdateView(UpdateView):
    model = Participation
    form_class = ParticipationForm
    template_name = 'tools/ptn_form.html'
    success_url = '/ptn_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(PtnUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class PtnCreateView(CreateView):
    model = Participation
    form_class = ParticipationForm
    template_name = 'tools/ptn_form.html'
    success_url = '/ptn_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(PtnCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class PtnDeleteView(DeleteView):
    model = Participation
    success_url = '/ptn_list'

@method_decorator(login_required, name='dispatch')
class PtyListView(ListView):
    model = Party
    context_object_name = 'partys'
    template_name = 'tools/pty_list.html'

@method_decorator(login_required, name='dispatch')
class PtyPublishView(TemplateView):
    model = Party
    template_name = 'tools/pty_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Party, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/pty_list')

@method_decorator(login_required, name='dispatch')
class PtyCopyView(TemplateView):
    model = Party
    template_name = 'tools/pty_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Party, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/pty_list')

@method_decorator(login_required, name='dispatch')
class PtyUpdateView(UpdateView):
    model = Party
    form_class = PartyForm
    template_name = 'tools/pty_form.html'
    success_url = '/pty_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(PtyUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class PtyCreateView(CreateView):
    model = Party
    form_class = PartyForm
    template_name = 'tools/pty_form.html'
    success_url = '/pty_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(PtyCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class PtyDeleteView(DeleteView):
    model = Party
    success_url = '/pty_list'

@method_decorator(login_required, name='dispatch')
class QtyListView(ListView):
    model = XdQuantity
    context_object_name = 'quantitys'
    template_name = 'tools/qty_list.html'

@method_decorator(login_required, name='dispatch')
class QtyPublishView(TemplateView):
    model = XdQuantity
    template_name = 'tools/qty_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdQuantity, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/qty_list')

@method_decorator(login_required, name='dispatch')
class QtyCopyView(TemplateView):
    model = XdQuantity
    template_name = 'tools/qty_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdQuantity, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/qty_list')

@method_decorator(login_required, name='dispatch')
class QtyUpdateView(UpdateView):
    model = XdQuantity
    form_class = QuantityForm
    template_name = 'tools/qty_form.html'
    success_url = '/qty_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(QtyUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class QtyCreateView(CreateView):
    model = XdQuantity
    form_class = QuantityForm
    template_name = 'tools/qty_form.html'
    success_url = '/qty_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(QtyCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class QtyDeleteView(DeleteView):
    model = XdQuantity
    success_url = '/qty_list'

@method_decorator(login_required, name='dispatch')
class RatListView(ListView):
    model = XdRatio
    context_object_name = 'ratios'
    template_name = 'tools/rat_list.html'

@method_decorator(login_required, name='dispatch')
class RatPublishView(TemplateView):
    model = XdRatio
    template_name = 'tools/rat_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdRatio, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/rat_list')

@method_decorator(login_required, name='dispatch')
class RatCopyView(TemplateView):
    model = XdRatio
    template_name = 'tools/rat_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdRatio, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/rat_list')

@method_decorator(login_required, name='dispatch')
class RatUpdateView(UpdateView):
    model = XdRatio
    form_class = RatioForm
    template_name = 'tools/rat_form.html'
    success_url = '/rat_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(RatUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class RatCreateView(CreateView):
    model = XdRatio
    form_class = RatioForm
    template_name = 'tools/rat_form.html'
    success_url = '/rat_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(RatCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class RatDeleteView(DeleteView):
    model = XdRatio
    success_url = '/rat_list'

@method_decorator(login_required, name='dispatch')
class RfrListView(ListView):
    model = ReferenceRange
    context_object_name = 'referenceranges'
    template_name = 'tools/rfr_list.html'

@method_decorator(login_required, name='dispatch')
class RfrPublishView(TemplateView):
    model = ReferenceRange
    template_name = 'tools/bool_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(ReferenceRange, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/rfr_list')

@method_decorator(login_required, name='dispatch')
class RfrCopyView(TemplateView):
    model = ReferenceRange
    template_name = 'tools/rfr_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(ReferenceRange, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/rfr_list')

@method_decorator(login_required, name='dispatch')
class RfrUpdateView(UpdateView):
    model = ReferenceRange
    form_class = ReferenceRangeForm
    template_name = 'tools/rfr_form.html'
    success_url = '/rfr_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(RfrUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class RfrCreateView(CreateView):
    model = ReferenceRange
    form_class = ReferenceRangeForm
    template_name = 'tools/rfr_form.html'
    success_url = '/rfr_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(RfrCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class RfrDeleteView(DeleteView):
    model = ReferenceRange
    success_url = '/rfr_list'

@method_decorator(login_required, name='dispatch')
class StrListView(ListView):
    model = XdString
    context_object_name = 'strings'
    template_name = 'tools/str_list.html'

@method_decorator(login_required, name='dispatch')
class StrPublishView(TemplateView):
    model = XdString
    template_name = 'tools/str_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdString, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/rfr_list')

@method_decorator(login_required, name='dispatch')
class StrCopyView(TemplateView):
    model = XdString
    template_name = 'tools/str_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdString, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/str_list')

@method_decorator(login_required, name='dispatch')
class StrUpdateView(UpdateView):
    model = XdString
    form_class = StringForm
    template_name = 'tools/str_form.html'
    success_url = '/str_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(StrUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class StrCreateView(CreateView):
    model = XdString
    form_class = StringForm
    template_name = 'tools/str_form.html'
    success_url = '/str_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(StrCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class StrDeleteView(DeleteView):
    model = XdString
    success_url = '/str_list'

@method_decorator(login_required, name='dispatch')
class TmpListView(ListView):
    model = XdTemporal
    context_object_name = 'temporals'
    template_name = 'tools/tmp_list.html'

@method_decorator(login_required, name='dispatch')
class TmpPublishView(TemplateView):
    model = XdTemporal
    template_name = 'tools/tmp_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdTemporal, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/tmp_list')

@method_decorator(login_required, name='dispatch')
class TmpCopyView(TemplateView):
    model = XdTemporal
    template_name = 'tools/tmp_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(XdTemporal, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/tmp_list')

@method_decorator(login_required, name='dispatch')
class TmpUpdateView(UpdateView):
    model = XdTemporal
    form_class = TemporalForm
    template_name = 'tools/tmp_form.html'
    success_url = '/tmp_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(TmpUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class TmpCreateView(CreateView):
    model = XdTemporal
    form_class = TemporalForm
    template_name = 'tools/tmp_form.html'
    success_url = '/tmp_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(TmpCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class TmpDeleteView(DeleteView):
    model = XdTemporal
    success_url = '/tmp_list'

@method_decorator(login_required, name='dispatch')
class UntListView(ListView):
    model = Units
    context_object_name = 'units'
    template_name = 'tools/unt_list.html'

@method_decorator(login_required, name='dispatch')
class UntPublishView(TemplateView):
    model = Units
    template_name = 'tools/unt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Units, id = kwargs['pk'])
        if "(***COPY***)" in obj.__str__():  # skip publishing a copy.
            msg = (obj.__str__() + " --Cannot publish a copy until it is edited.", messages.ERROR)
        else:
            msg = obj.publish(request)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/unt_list')

@method_decorator(login_required, name='dispatch')
class UntCopyView(TemplateView):
    model = Units
    template_name = 'tools/unt_list.html'

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Units, id = kwargs['pk'])
        new_obj = obj
        new_obj.creator = get_object_or_404(Modeler, user=self.request.user)
        new_obj.edited_by = get_object_or_404(Modeler, user=self.request.user)
        new_obj.pk = None
        new_obj.label = obj.label + " (***COPY***)"
        new_obj.published = False
        new_obj.schema_code = ''
        new_obj.ct_id = cuid()
        new_obj.adapter_ctid = cuid()
        new_obj.save()
        msg = (obj.__str__() + " was Copied!", messages.SUCCESS)
        messages.add_message(request, msg[1], msg[0])
        return HttpResponseRedirect('/unt_list')

@method_decorator(login_required, name='dispatch')
class UntUpdateView(UpdateView):
    model = Units
    form_class = UnitsForm
    template_name = 'tools/unt_form.html'
    success_url = '/unt_list'

    def form_valid(self, form):
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(UntUpdateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class UntCreateView(CreateView):
    model = Units
    form_class = UnitsForm
    template_name = 'tools/unt_form.html'
    success_url = '/unt_list'

    def form_valid(self, form):
        form.instance.creator = get_object_or_404(Modeler, user=self.request.user)
        form.instance.edited_by = get_object_or_404(Modeler, user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(UntCreateView, self).get_form_kwargs(**kwargs)
        form_kwargs["current_user"] = self.request.user
        form_kwargs["default_prj"] = get_object_or_404(Modeler, user=self.request.user).project
        form_kwargs["filter_prj"] = get_object_or_404(Modeler, user=self.request.user).prj_filter
        return form_kwargs


@method_decorator(login_required, name='dispatch')
class UntDeleteView(DeleteView):
    model = Units
    success_url = '/unt_list'


class ModUpdateView(UpdateView):
    model = Modeler
    form_class = ModelerForm
    template_name = 'tools/mod_form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ModUpdateView, self).get_context_data(**kwargs)
        context['whole_name'] = self.request.user.first_name + ' ' + self.request.user.last_name
        return context

