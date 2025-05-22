"""itt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from dmgen.views import IndexView, ToolsView, DMListView, DMGenerateView, DMCopyView, DMUpdateView, DMCreateView, DMDeleteView, \
                                   AttListView, AttPublishView, AttCopyView, AttCreateView, AttUpdateView, AttDeleteView, \
                                   AudListView, AudPublishView, AudCopyView, AudCreateView, AudUpdateView, AudDeleteView, \
                                   BoolListView, BoolPublishView, BoolCopyView, BoolCreateView, BoolUpdateView, BoolDeleteView, \
                                   CluListView, CluPublishView, CluCopyView, CluCreateView, CluUpdateView, CluDeleteView, \
                                   CntListView, CntPublishView, CntCopyView, CntCreateView, CntUpdateView, CntDeleteView, \
                                   FilListView, FilPublishView, FilCopyView, FilCreateView, FilUpdateView, FilDeleteView, \
                                   FltListView, FltPublishView, FltCopyView, FltCreateView, FltUpdateView, FltDeleteView, \
                                   IntListView, IntPublishView, IntCopyView, IntCreateView, IntUpdateView, IntDeleteView, \
                                   LnkListView, LnkPublishView, LnkCopyView, LnkCreateView, LnkUpdateView, LnkDeleteView, \
                                   OrdListView, OrdPublishView, OrdCopyView, OrdCreateView, OrdUpdateView, OrdDeleteView, \
                                   PtnListView, PtnPublishView, PtnCopyView, PtnCreateView, PtnUpdateView, PtnDeleteView, \
                                   PtyListView, PtyPublishView, PtyCopyView, PtyCreateView, PtyUpdateView, PtyDeleteView, \
                                   QtyListView, QtyPublishView, QtyCopyView, QtyCreateView, QtyUpdateView, QtyDeleteView, \
                                   RatListView, RatPublishView, RatCopyView, RatCreateView, RatUpdateView, RatDeleteView, \
                                   RfrListView, RfrPublishView, RfrCopyView, RfrCreateView, RfrUpdateView, RfrDeleteView, \
                                   StrListView, StrPublishView, StrCopyView, StrCreateView, StrUpdateView, StrDeleteView, \
                                   TmpListView, TmpPublishView, TmpCopyView, TmpCreateView, TmpUpdateView, TmpDeleteView, \
                                   UntListView, UntPublishView, UntCopyView, UntCreateView, UntUpdateView, UntDeleteView, ModUpdateView
from translator.views import DMDListView, DMDUpdateView, DMDCreateView, DMDDeleteView, \
                             RecListView, RecUpdateView, RecCreateView, RecDeleteView


admin.autodiscover()

"""
API URLS look like this on the dev machine:

http://127.0.0.1:8000/api/v1/xdboolean
or for JSON
http://127.0.0.1:8000/api/v1/xdboolean?format=json
"""
urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^tools/', ToolsView.as_view(), name='tools'),
    url(r'^select2/', include('django_select2.urls')),

    path('dm_list/', DMListView.as_view(), name = 'dm_list'),
    path('dm_generate/<int:pk>', DMGenerateView.as_view(), name='dm_generate'),
    path('dm_copy/<int:pk>', DMCopyView.as_view(), name='dm_copy'),
    path('dm_form/<int:pk>/', DMUpdateView.as_view(), name='dm_form'),
    path('dm_create/', DMCreateView.as_view(), name='dm_create'),
    path('dm_delete/<int:pk>/', DMDeleteView.as_view(), name='dm_delete'),

    path('att_list/', AttListView.as_view(), name = 'att_list'),
    path('att_publish/<int:pk>', AttPublishView.as_view(), name='att_publish'),
    path('att_copy/<int:pk>', AttCopyView.as_view(), name='att_copy'),
    path('att_form/<int:pk>/', AttUpdateView.as_view(), name='att_form'),
    path('att_create/', AttCreateView.as_view(), name='att_create'),
    path('att_delete/<int:pk>/', AttDeleteView.as_view(), name='att_delete'),

    path('aud_list/', AudListView.as_view(), name = 'aud_list'),
    path('aud_publish/<int:pk>', AudPublishView.as_view(), name='aud_publish'),
    path('aud_copy/<int:pk>', AudCopyView.as_view(), name='aud_copy'),
    path('aud_form/<int:pk>/', AudUpdateView.as_view(), name='aud_form'),
    path('aud_create/', AudCreateView.as_view(), name='aud_create'),
    path('aud_delete/<int:pk>/', AudDeleteView.as_view(), name='aud_delete'),

    path('bool_list/', BoolListView.as_view(), name = 'bool_list'),
    path('bool_publish/<int:pk>', BoolPublishView.as_view(), name='bool_publish'),
    path('bool_copy/<int:pk>', BoolCopyView.as_view(), name='bool_copy'),
    path('bool_form/<int:pk>/', BoolUpdateView.as_view(), name='bool_form'),
    path('bool_create/', BoolCreateView.as_view(), name='bool_create'),
    path('bool_delete/<int:pk>/', BoolDeleteView.as_view(), name='bool_delete'),

    path('clu_list/', CluListView.as_view(), name = 'clu_list'),
    path('clu_publish/<int:pk>', CluPublishView.as_view(), name='clu_publish'),
    path('clu_copy/<int:pk>', CluCopyView.as_view(), name='clu_copy'),
    path('clu_form/<int:pk>/', CluUpdateView.as_view(), name='clu_form'),
    path('clu_create/', CluCreateView.as_view(), name='clu_create'),
    path('clu_delete/<int:pk>/', CluDeleteView.as_view(), name='clu_delete'),

    path('cnt_list/', CntListView.as_view(), name = 'cnt_list'),
    path('cnt_publish/<int:pk>', CntPublishView.as_view(), name='cnt_publish'),
    path('cnt_copy/<int:pk>', CntCopyView.as_view(), name='cnt_copy'),
    path('cnt_form/<int:pk>/', CntUpdateView.as_view(), name='cnt_form'),
    path('cnt_create/', CntCreateView.as_view(), name='cnt_create'),
    path('cnt_delete/<int:pk>/', CntDeleteView.as_view(), name='cnt_delete'),

    path('fil_list/', FilListView.as_view(), name = 'fil_list'),
    path('fil_publish/<int:pk>', FilPublishView.as_view(), name='fil_publish'),
    path('fil_copy/<int:pk>', FilCopyView.as_view(), name='fil_copy'),
    path('fil_form/<int:pk>/', FilUpdateView.as_view(), name='fil_form'),
    path('fil_create/', FilCreateView.as_view(), name='fil_create'),
    path('fil_delete/<int:pk>/', FilDeleteView.as_view(), name='fil_delete'),

    path('flt_list/', FltListView.as_view(), name = 'flt_list'),
    path('flt_publish/<int:pk>', FltPublishView.as_view(), name='flt_publish'),
    path('flt_copy/<int:pk>', FltCopyView.as_view(), name='flt_copy'),
    path('flt_form/<int:pk>/', FltUpdateView.as_view(), name='flt_form'),
    path('flt_create/', FltCreateView.as_view(), name='flt_create'),
    path('flt_delete/<int:pk>/', FltDeleteView.as_view(), name='flt_delete'),

    path('int_list/', IntListView.as_view(), name = 'int_list'),
    path('int_publish/<int:pk>', IntPublishView.as_view(), name='int_publish'),
    path('int_copy/<int:pk>', IntCopyView.as_view(), name='int_copy'),
    path('int_form/<int:pk>/', IntUpdateView.as_view(), name='int_form'),
    path('int_create/', IntCreateView.as_view(), name='int_create'),
    path('int_delete/<int:pk>/', IntDeleteView.as_view(), name='int_delete'),

    path('lnk_list/', LnkListView.as_view(), name = 'lnk_list'),
    path('lnk_publish/<int:pk>', LnkPublishView.as_view(), name='lnk_publish'),
    path('lnk_copy/<int:pk>', LnkCopyView.as_view(), name='lnk_copy'),
    path('lnk_form/<int:pk>/', LnkUpdateView.as_view(), name='lnk_form'),
    path('lnk_create/', LnkCreateView.as_view(), name='lnk_create'),
    path('lnk_delete/<int:pk>/', LnkDeleteView.as_view(), name='lnk_delete'),

    path('ord_list/', OrdListView.as_view(), name = 'ord_list'),
    path('ord_publish/<int:pk>', OrdPublishView.as_view(), name='ord_publish'),
    path('ord_copy/<int:pk>', OrdCopyView.as_view(), name='ord_copy'),
    path('ord_form/<int:pk>/', OrdUpdateView.as_view(), name='ord_form'),
    path('ord_create/', OrdCreateView.as_view(), name='ord_create'),
    path('ord_delete/<int:pk>/', OrdDeleteView.as_view(), name='ord_delete'),

    path('ptn_list/', PtnListView.as_view(), name = 'ptn_list'),
    path('ptn_publish/<int:pk>', PtnPublishView.as_view(), name='ptn_publish'),
    path('ptn_copy/<int:pk>', PtnCopyView.as_view(), name='ptn_copy'),
    path('ptn_form/<int:pk>/', PtnUpdateView.as_view(), name='ptn_form'),
    path('ptn_create/', PtnCreateView.as_view(), name='ptn_create'),
    path('ptn_delete/<int:pk>/', PtnDeleteView.as_view(), name='ptn_delete'),

    path('pty_list/', PtyListView.as_view(), name = 'pty_list'),
    path('pty_publish/<int:pk>', PtyPublishView.as_view(), name='pty_publish'),
    path('pty_copy/<int:pk>', PtyCopyView.as_view(), name='pty_copy'),
    path('pty_form/<int:pk>/', PtyUpdateView.as_view(), name='pty_form'),
    path('pty_create/', PtyCreateView.as_view(), name='pty_create'),
    path('pty_delete/<int:pk>/', PtyDeleteView.as_view(), name='pty_delete'),

    path('qty_list/', QtyListView.as_view(), name = 'qty_list'),
    path('qty_publish/<int:pk>', QtyPublishView.as_view(), name='qty_publish'),
    path('qty_copy/<int:pk>', QtyCopyView.as_view(), name='qty_copy'),
    path('qty_form/<int:pk>/', QtyUpdateView.as_view(), name='qty_form'),
    path('qty_create/', QtyCreateView.as_view(), name='qty_create'),
    path('qty_delete/<int:pk>/', QtyDeleteView.as_view(), name='qty_delete'),

    path('rat_list/', RatListView.as_view(), name = 'rat_list'),
    path('rat_publish/<int:pk>', RatPublishView.as_view(), name='rat_publish'),
    path('rat_copy/<int:pk>', RatCopyView.as_view(), name='rat_copy'),
    path('rat_form/<int:pk>/', RatUpdateView.as_view(), name='rat_form'),
    path('rat_create/', RatCreateView.as_view(), name='rat_create'),
    path('rat_delete/<int:pk>/', RatDeleteView.as_view(), name='rat_delete'),

    path('rfr_list/', RfrListView.as_view(), name = 'rfr_list'),
    path('rfr_publish/<int:pk>', RfrPublishView.as_view(), name='rfr_publish'),
    path('rfr_copy/<int:pk>', RfrCopyView.as_view(), name='rfr_copy'),
    path('rfr_form/<int:pk>/', RfrUpdateView.as_view(), name='rfr_form'),
    path('rfr_create/', RfrCreateView.as_view(), name='rfr_create'),
    path('rfr_delete/<int:pk>/', RfrDeleteView.as_view(), name='rfr_delete'),

    path('str_list/', StrListView.as_view(), name = 'str_list'),
    path('str_publish/<int:pk>', StrPublishView.as_view(), name='str_publish'),
    path('str_copy/<int:pk>', StrCopyView.as_view(), name='str_copy'),
    path('str_form/<int:pk>/', StrUpdateView.as_view(), name='str_form'),
    path('str_create/', StrCreateView.as_view(), name='str_create'),
    path('str_delete/<int:pk>/', StrDeleteView.as_view(), name='str_delete'),

    path('tmp_list/', TmpListView.as_view(), name = 'tmp_list'),
    path('tmp_publish/<int:pk>', TmpPublishView.as_view(), name='tmp_publish'),
    path('tmp_copy/<int:pk>', TmpCopyView.as_view(), name='tmp_copy'),
    path('tmp_form/<int:pk>/', TmpUpdateView.as_view(), name='tmp_form'),
    path('tmp_create/', TmpCreateView.as_view(), name='tmp_create'),
    path('tmp_delete/<int:pk>/', TmpDeleteView.as_view(), name='tmp_delete'),

    path('unt_list/', UntListView.as_view(), name = 'unt_list'),
    path('unt_publish/<int:pk>', UntPublishView.as_view(), name='unt_publish'),
    path('unt_copy/<int:pk>', UntCopyView.as_view(), name='unt_copy'),
    path('unt_form/<int:pk>/', UntUpdateView.as_view(), name='unt_form'),
    path('unt_create/', UntCreateView.as_view(), name='unt_create'),
    path('unt_delete/<int:pk>/', UntDeleteView.as_view(), name='unt_delete'),

    #  Translator
    path('dmd_list/', DMDListView.as_view(), name = 'dmd_list'),
    path('dmd_form/<int:pk>/', DMDUpdateView.as_view(), name='dmd_form'),
    path('dmd_create/', DMDCreateView.as_view(), name='dmd_create'),
    path('dmd_delete/<int:pk>/', DMDDeleteView.as_view(), name='dmd_delete'),

    path('rec_list/', RecListView.as_view(), name = 'rec_list'),
    path('rec_form/<int:pk>/', RecUpdateView.as_view(), name='rec_form'),
    path('rec_create/', RecCreateView.as_view(), name='rec_create'),
    path('rec_delete/<int:pk>/', RecDeleteView.as_view(), name='rec_delete'),

    path('mod_form/<int:pk>/', ModUpdateView.as_view(), name='mod_form'),

]
