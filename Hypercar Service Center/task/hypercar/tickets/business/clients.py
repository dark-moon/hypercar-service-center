from collections import deque

CHANGE_OIL_KEY = 'change_oil'
INFLATE_TIRES_KEY = 'inflate_tires'
DIAGNOSTIC_KEY = 'diagnostic'


class Ticket(object):

    def __init__(self, service_type, ticket_number, waiting_time):
        self.service_type = service_type
        self.ticket_number = ticket_number
        self.waiting_time = waiting_time


class ClientsQueue(object):

    current_client = None

    def __init__(self):
        self.__tickets_count = 0
        self.__oil_queue = deque()
        self.__tires_queue = deque()
        self.__diagnostic_queue = deque()
        self.lines_of_cars = {
            CHANGE_OIL_KEY: deque(),
            INFLATE_TIRES_KEY: deque(),
            DIAGNOSTIC_KEY: deque()
        }

    def add_client(self, service_type):
        self.__tickets_count += 1
        ticket = Ticket(service_type, self.__tickets_count, self.__waiting_time(service_type))
        self.lines_of_cars[service_type].appendleft(ticket)
        return ticket

    def process_next(self):
        if not self.__oil_queue and not self.__tires_queue and not self.__diagnostic_queue:
            self.__oil_queue = self.lines_of_cars.get(CHANGE_OIL_KEY)
            self.__tires_queue = self.lines_of_cars.get(INFLATE_TIRES_KEY)
            self.__diagnostic_queue = self.lines_of_cars.get(DIAGNOSTIC_KEY)
        self.current_client = self.pop_next_client()

    def peek_next_client(self):
        if len(self.__oil_queue) > 0:
            return self.__oil_queue[len(self.__oil_queue) - 1]
        elif len(self.__tires_queue) > 0:
            return self.__tires_queue[len(self.__tires_queue) - 1]
        elif len(self.__diagnostic_queue) > 0:
            return self.__diagnostic_queue[len(self.__diagnostic_queue) - 1]
        else:
            return None

    def pop_next_client(self):
        self.__tickets_count -= 1
        if len(self.__oil_queue) > 0:
            return self.__oil_queue.pop()
        elif len(self.__tires_queue) > 0:
            return self.__tires_queue.pop()
        elif len(self.__diagnostic_queue) > 0:
            return self.__diagnostic_queue.pop()
        else:
            self.__tickets_count += 1
            return None

    def __waiting_time(self, service_type):
        oil_waiting = len(self.lines_of_cars.get(CHANGE_OIL_KEY)) * 2
        tires_waiting = len(self.lines_of_cars.get(INFLATE_TIRES_KEY)) * 5 + oil_waiting
        diagnostics_waiting = len(self.lines_of_cars.get(DIAGNOSTIC_KEY)) * 30 + tires_waiting

        if service_type == CHANGE_OIL_KEY:
            return oil_waiting
        elif service_type == INFLATE_TIRES_KEY:
            return tires_waiting
        elif service_type == DIAGNOSTIC_KEY:
            return diagnostics_waiting
        else:
            return 0
