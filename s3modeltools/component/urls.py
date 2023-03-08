from django.urls import path
from .views import AttestationList, AttestationCreate, AttestationUpdate, AuditList, AuditCreate, AuditUpdate


urlpatterns = [
    path('attestation/', AttestationList.as_view(), name='attestation_list'),
    path('attestation/create/', AttestationCreate.as_view(), name='attestation_create'),
    path('attestation/update/<int:pk>/', AttestationUpdate.as_view(), name='attestation_update'),
    path('audit/', AuditList.as_view(), name='audit_list'),
    path('audit/create/', AuditCreate.as_view(), name='audit_create'),
    path('audit/update/<int:pk>/', AuditUpdate.as_view(), name='audit_update'),
    ]

