from django.urls import path

from . import views

urlpatterns = [
    path('', views.TheModelView, name='TheModelView'),
    path('/<str:name>', views.StationID, name='StationID'),
    ]