from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car', views.car, name='car'),
    path('property', views.propertys , name='property'),
    path(r'^signup/$', views.signup, name='signup'),
    path('import/', views.carCreate, name='import'),
    path('detail/<int:id>', views.detailView, name='detail'),
    path(r'^search/$', views.search, name='search'),

]