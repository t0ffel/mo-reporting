from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'assignments/unrelated$', views.get_unrelated_assignments, name='get_unrelated_assignments'),
    url(r'assignments/(?P<project_id>[\w-]+)$', views.get_assignments, name='get_assignments'),
    url(r'projects$', views.get_current_projects, name='get_current_projects')
]
