from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('', views.units, name='units'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),


    path('logs/', views.logs, name='logs'),
    path('logs/<int:id>', views.log, name='log'),
    # path('logs/errors/', views.errors, 'errors'),

    path('drivers/', views.drivers, name='drivers'),
    path('new-driver/', views.new_driver, name='new-driver'),
    path('edit-driver/<int:id>', views.edit_driver, name='edit-driver'),
    # path('edit-detail/<int:id>', views.edit_detail, name='edit-detail'),

    path('vehicles/', views.vehicles, name='vehicles'),
    path('new-vehicle/', views.new_vehicle, name='new-vehicle'),
    path('edit-vehicle/<str:id>', views.edit_vehicle, name='edit-vehicle'),

]
