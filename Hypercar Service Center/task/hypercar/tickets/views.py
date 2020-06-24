from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from .business.clients import Ticket
from .business.clients import ClientsQueue

change_oil = 'Change oil'
inflate_tires = 'Inflate tires'
diagnostic = 'Get diagnostic test'

clients_queue = ClientsQueue()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/welcome.html')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        menu = {
            'services': {change_oil: 'get_ticket/change_oil',
                         inflate_tires: 'get_ticket/inflate_tires',
                         diagnostic: 'get_ticket/diagnostic'}
        }
        return render(request, 'tickets/menu.html', context=menu)


class ServiceView(View):

    def get(self, request, service_type, *args, **kwargs):
        current_ticket = clients_queue.add_client(service_type)
        return render(request, 'tickets/ticket.html', context={'ticket': current_ticket})


class OperatorsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/operators_menu.html', clients_queue.lines_of_cars)

    def post(self, request, *args, **kwargs):
        clients_queue.process_next()
        return redirect('/next')


class NextView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'tickets/next_client.html', {
            'next_client': clients_queue.current_client
        })


