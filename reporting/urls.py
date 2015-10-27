from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'unrelated$', views.get_unrelated_assignments, name='get_unrelated_assignments')
]
