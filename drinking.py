import random
import time
from mpi4py import MPI


class Philosopher(object):
    def __init__(self, index):
        self.index = index
        self.hands = {
            'L': 'D',
            'R': None
        }
        self.neighbours = {
            'L': size - 1 if index == 0 else index - 1,
            'R': 0 if index == size - 1 else index + 1,
        }
        self.listeners = {
            'L': comm.recv(dest=self.neighbours['L']),
            'R': comm.recv(dest=self.neighbours['R'])
        }
        self.requests = set()

    def start(self):
        while(True):
            self.sleep()
            self.get_forks()
            self.eat()

    def sleep(self):
        print ("{0}: sleeping".format(self.index))
        for i in range(random.randint(10, 40)):
            time.sleep(0.1)
            self.check_requests()

    def eat(self):
        print ("{0}: I'm starting to eat".format(self.index))
        time.sleep(random.uniform(1, 2))
        self.hands['L'] = "D"
        self.hands['R'] = "D"
        print ("{0}: I ate".format(self.index))

    def get_forks(self):
        # added a delay to reduce the resending of identical messages
        delay = 6
        while not self.has_both_forks():
            for side, value in self.hands.items():
                if not value and delay > 5:
                    comm.send("gimme", dest=self.neighbours[side])
                    print ("{0}: I'm asking for fork {1}".format(self.index, self.neighbours[side]))
                    delay = 0
            self.check_requests()
            time.sleep(random.uniform(0, 2))
            delay += 1

    def check_requests(self):
        # first handle the old requests
        for side in self.requests:
            self.handle_request(side)

        self.requests.clear()

        # then check if there are any new requests
        for side in self.neighbours:
            received, message = self.listeners[side].test()
            if received:
                self.handle_request(side, message)
                self.listeners[side] = comm.recv(dest=self.neighbours[side])

    def handle_request(self, side, message="gimme"):
        # if i got a fork, put it in my hand
        if message in ['C', 'D']:
            self.hands[side] = message
            print ("{0}: Got fork {1}".format(self.index, self.neighbours[side]))
        else:
            # if the fork is requested and it's dirty, clean it and pass it
            if self.hands[side] == "D":
                comm.send("C", dest=self.neighbours[side])
                self.hands[side] = None
            # if it's clean, keep it and remember the request
            else:
                if side not in self.requests:
                    self.requests.add(side)

    def has_both_forks(self):
        return all(self.hands.values())


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
philosopher = Philosopher(rank)
philosopher.start()
