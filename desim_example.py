from abc import abstractmethod

import matplotlib.pyplot as plt
from numpy import random

from desim import DiscreteEvent, DiscreteEventQueue, run_to_end

# System ----------------------------------------------------------------------------------------------


class Store:
    def __init__(self):
        self.state = "closed"
        self.customers = 0

    def open(self):
        self.state = "open"

    def close(self):
        self.state = "closed"

    def is_open(self):
        return self.state == "open"

    def customer_enters(self):
        self.customers += 1

    def customer_leaves(self):
        self.customers -= 1


class Stats:
    def __init__(self, mean_arrival_time, mean_shopping_time):
        self.mean_arrival_time = mean_arrival_time
        self.mean_shopping_time = mean_shopping_time

    def random_arrival_time(self):
        return random.exponential(self.mean_arrival_time)

    def random_shopping_time(self):
        return random.exponential(self.mean_shopping_time)


# Events ----------------------------------------------------------------------------------------------


class DiscreteEventBase(DiscreteEvent):
    logs_enabled = False

    def __init__(self, t):
        super().__init__(t)

    def _run(self, env):
        if DiscreteEventBase.logs_enabled:
            print(f"{self.__class__.__name__} (at {self.t:.1f})")

        store, stats = env
        return self._run_internal(store, stats)

    @abstractmethod
    def _run_internal(self, store: Store, stats: Stats): ...


class OpenStoreEvent(DiscreteEventBase):
    def __init__(self, t):
        super().__init__(t)

    def _run_internal(self, store, stats):
        store.open()
        first_arrival = CustomerArrivalEvent(self._after(stats.random_arrival_time()))
        return [first_arrival]


class CloseStoreEvent(DiscreteEventBase):
    def __init__(self, t):
        super().__init__(t)

    def _run_internal(self, store, stats):
        store.close()
        return []


class CustomerArrivalEvent(DiscreteEventBase):
    def __init__(self, t):
        super().__init__(t)

    def _run_internal(self, store, stats):
        if store.is_open():
            store.customer_enters()
            print(f"{store.customers=}")
            next_arrival = CustomerArrivalEvent(self._after(stats.random_arrival_time()))
            customer_done = CustomerDoneEvent(self._after(stats.random_shopping_time()))
            return [next_arrival, customer_done]

        else:
            print("Oops, too late")
            return []


class CustomerDoneEvent(DiscreteEventBase):
    def __init__(self, t):
        super().__init__(t)

    def _run_internal(self, store, stats):
        store.customer_leaves()
        print(f"{store.customers=}")
        return []


class ChangeArrivalTimeEvent(DiscreteEventBase):
    def __init__(self, t, arrival_time):
        super().__init__(t)
        self.arrival_time = arrival_time

    def _run_internal(self, store, stats):
        stats.mean_arrival_time = self.arrival_time
        return []


# Cases -----------------------------------------------------------------------------------------------


def case_study_1():
    store = Store()
    stats = Stats(mean_arrival_time=1, mean_shopping_time=5)

    queue = DiscreteEventQueue()
    queue.add_events(
        [
            OpenStoreEvent(0),
            ChangeArrivalTimeEvent(20, 0.5),  # rush-hour
            ChangeArrivalTimeEvent(45, 1.5),  # end of rush-hour
            CloseStoreEvent(60),
        ]
    )

    t = []
    customers = []

    def callback(_, __):
        t.append(queue.t)
        customers.append(store.customers)

    run_to_end(queue, (store, stats), callback)

    return t, customers


# main ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    DiscreteEventBase.logs_enabled = True

    n_sim = 100

    for i in range(n_sim):
        print(f"------------------------ sim {i+1} / {n_sim} ------------------------")
        t, customers = case_study_1()
        plt.step(t, customers, where="pre", color="black", alpha=0.1)

    plt.xlabel("time (min)")
    plt.ylabel("customers")
    plt.show()
