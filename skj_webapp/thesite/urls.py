from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employee', views.employee, name='employee'),
    path('busyness', views.busyness, name='busyness'),
    path('sellTicket', views.sellTicket, name='sellTicket'),
    path('sellTicketForm', views.sellTicketForm, name='sellTicketForm'),
    path('validateTicket', views.validateTicket, name='validateTicket'),
    path('validateTicketForm', views.validateTicketForm, name='validateTicketForm'),
    path('delEmployee', views.delEmployee, name='delEmployee'),
    path('editEmployee', views.editEmployee, name='editEmployee'),
    path('editEmployeeForm', views.editEmployeeForm, name='editEmployeeForm'),
    path('owner', views.owner, name='owner'),
    path('editPerformance', views.editPerformance, name='editPerformance'),
    path('deletePerformance', views.deletePerformance, name='deletePerformance'),
    path('addPerformance', views.addPerformance, name='addPerformance'),
    path('addEmployee', views.addEmployee, name='addEmployee'),
    path('addEmployeeForm', views.addEmployeeForm, name='addEmployeeForm'),
    path('festival', views.festival, name='festival'),
    path('festivalForm', views.festivalForm, name='festivalForm'),
    path('ticketList', views.ticketList, name='ticketList'),
    path('ticketListForm', views.ticketListForm, name='ticketListForm'),
    path('festival/<int:fest_id>', views.festival_info),
]
