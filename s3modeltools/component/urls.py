from django.urls import path
from .views import AttestationList, AttestationCreate, AttestationUpdate, AuditList, AuditCreate, AuditUpdate, \
    BooleanList, BooleanCreate, BooleanUpdate, ClusterList, ClusterCreate, ClusterUpdate, CountList, CountCreate, CountUpdate, \
    DataModelList, DataModelCreate, DataModelUpdate, FileList, FileCreate, FileUpdate, FloatList, FloatCreate, FloatUpdate  
    


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
    ]

