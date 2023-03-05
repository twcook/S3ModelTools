from django.urls import path
from .views import AttestationList, AttestationCreate, AttestationUpdate


urlpatterns = [
    path('attestation/', AttestationList.as_view(), name='attestation_list'),
    path('attestation/create/', AttestationCreate.as_view(), name='attestation_create'),
    path('attestation/update/<int:pk>/', AttestationUpdate.as_view(), name='attestation_update'),
    ]

