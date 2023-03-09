from django.urls import path

from .views import ProjectListView, ProjectCreate, ProjectUpdate, ModelerListView, ModelerCreate, ModelerUpdate


urlpatterns = [
    path('project/', ProjectListView.as_view(), name='project_list'),
    path('project/create/', ProjectCreate.as_view(), name='project_create'),
    path('project/update/<int:pk>/', ProjectUpdate.as_view(), name='project_update'),
    path('modeler/', ModelerListView.as_view(), name='modeler_list'),
    path('modeler/create/', ModelerCreate.as_view(), name='modeler_create'),
    path('modeler/update/<int:pk>/', ModelerUpdate.as_view(), name='modeler_update'),
    ]

