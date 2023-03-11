from django.urls import path
from .views import AttestationList, AttestationCreate, AttestationUpdate, AuditList, AuditCreate, AuditUpdate, \
    BooleanList, BooleanCreate, BooleanUpdate, ClusterList, ClusterCreate, ClusterUpdate, CountList, CountCreate, CountUpdate, \
    DataModelList, DataModelCreate, DataModelUpdate, FileList, FileCreate, FileUpdate, FloatList, FloatCreate, FloatUpdate, \
    IntervalList, IntervalCreate, IntervalUpdate, LinkList, LinkCreate, LinkUpdate, NamespaceList, NamespaceCreate, NamespaceUpdate, \
    OrdinalList, OrdinalCreate, OrdinalUpdate   
    


urlpatterns = [
    path('attestation/', AttestationList.as_view(), name='attestation_list'),
    path('attestation/create/', AttestationCreate.as_view(), name='attestation_create'),
    path('attestation/update/<int:pk>/', AttestationUpdate.as_view(), name='attestation_update'),
    path('audit/', AuditList.as_view(), name='audit_list'),
    path('audit/create/', AuditCreate.as_view(), name='audit_create'),
    path('audit/update/<int:pk>/', AuditUpdate.as_view(), name='audit_update'),
    path('boolean/', BooleanList.as_view(), name='boolean_list'),
    path('boolean/create/', BooleanCreate.as_view(), name='boolean_create'),
    path('boolean/update/<int:pk>/', BooleanUpdate.as_view(), name='boolean_update'),
    path('cluster/', ClusterList.as_view(), name='cluster_list'),
    path('cluster/create/', ClusterCreate.as_view(), name='cluster_create'),
    path('cluster/update/<int:pk>/', ClusterUpdate.as_view(), name='cluster_update'),
    path('count/', CountList.as_view(), name='count_list'),
    path('count/create/', CountCreate.as_view(), name='count_create'),
    path('count/update/<int:pk>/', CountUpdate.as_view(), name='count_update'),
    path('datamodel/', DataModelList.as_view(), name='datamodel_list'),
    path('datamodel/create/', DataModelCreate.as_view(), name='datamodel_create'),
    path('datamodel/update/<int:pk>/', DataModelUpdate.as_view(), name='datamodel_update'),
    path('file/', FileList.as_view(), name='file_list'),
    path('file/create/', FileCreate.as_view(), name='file_create'),
    path('file/update/<int:pk>/', FileUpdate.as_view(), name='file_update'),
    path('float/', FloatList.as_view(), name='float_list'),
    path('float/create/', FloatCreate.as_view(), name='float_create'),
    path('float/update/<int:pk>/', FloatUpdate.as_view(), name='float_update'),
    path('interval/', IntervalList.as_view(), name='interval_list'),
    path('interval/create/', IntervalCreate.as_view(), name='interval_create'),
    path('interval/update/<int:pk>/', IntervalUpdate.as_view(), name='interval_update'),
    path('link/', LinkList.as_view(), name='link_list'),
    path('link/create/', LinkCreate.as_view(), name='link_create'),
    path('link/update/<int:pk>/', LinkUpdate.as_view(), name='link_update'),
    path('namespace/', NamespaceList.as_view(), name='namespace_list'),
    path('namespace/create/', NamespaceCreate.as_view(), name='namespace_create'),
    path('namespace/update/<int:pk>/', NamespaceCreate.as_view(), name='namespace_update'),
    path('ordinal/', OrdinalList.as_view(), name='ordinal_list'),
    path('ordinal/create/', OrdinalCreate.as_view(), name='ordinal_create'),
    path('ordinal/update/<int:pk>/', OrdinalUpdate.as_view(), name='ordinal_update'),
    ]

