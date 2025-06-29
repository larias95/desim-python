# DeSim (Discrete Event Simulator)

A Discrete Event Simulation (DES) library for modeling systems where state changes occur at discrete points in time.

## Description

**DeSim** is a flexible Discrete Event Simulation (DES) library built for modeling systems where state changes occur at specific points in time. At its core is a queue of events that governs how the simulation evolves, processing scheduled actions in chronological order to reflect changes in system state. This method allows **DeSim** to simulate dynamic environments with precision and efficiency, focusing computation only when activity occurs, and so, mirroring the complexity of real-world systems without imposing rigid structures.

Using **DeSim** involves defining system behavior through object-oriented design. At the core of the library is a `DiscreteEvent` base class, which users extend to model specific types of events. Each derived event class encapsulates the logic needed to evolve the system, such as modifying state variables, scheduling future events, or interacting with other components. This design encourages clean separation of concerns and makes simulations more maintainable and reusable. By modeling system dynamics as a series of interacting event classes, **DeSim** allows users to build rich, modular simulations that are both intuitive and scalable.

### Features

- 📦 OOP: Object-oriented paradigm was taken in mind in order to allow flexibility while modeling dynamic systems.
- ⏱️ Discrete time: Time updates are based on occurrences of events, and not on `while True: update(deltatime)` approaches.
- ⏩ Queue-based: Events are retrieved from a priority queue that sorts them based on their time of occurrence.
- 🍃 Lightweight: **DeSim** has no external dependencies.

### Quick Example

Suppose we want to model a store and the flow of customers that arrive over time. We can model this by implementing events like: *the store opened*, *a customer arrived*, *a customer is ready to pay and leave the store*, *the store closed*, etc. So, the execution of one *customer arrival* could lead to the next one, and also to generate an event for when *that customer is done*. We just need to override the `_run(self, env)` method from the `DiscreteEvent` base class to model all of those interactions.

```python
from desim import DiscreteEvent, DiscreteEventQueue, run_to_end

#
# ...
#

class CustomerArrivalEvent(DiscreteEvent):
    def __init__(self, t):
        super().__init__(t)

    def _run(self, env):
        store, stats = env

        if store.is_open():
            store.customer_enters()
            print(f"{store.customers=}")

            next_arrival = CustomerArrivalEvent(self._after(stats.random_arrival_time()))
            customer_done = CustomerDoneEvent(self._after(stats.random_shopping_time()))
            return [next_arrival, customer_done]

        else:
            print("Oops, too late")
            return []

#
# ...
#

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
```

## Installation

You can install **DeSim** using either **PyPI** or clone it from **GitHub**.

### From PyPI (recommended):

```sh
pip install desim-python
```

### From GitHub:

```sh
git clone https://github.com/larias95/desim-python.git
cd desim-python
pip install .
```

## Examples

After installation you can run examples from the `examples/` folder. E.g: `python store_example.py`.

You may need to install some dependencies before running the examples by using `pip install -r requirements.txt` from `examples/` folder.

## Links

- [PyPI](https://pypi.org/project/desim-python/)
- [GitHub](https://github.com/larias95/desim-python)
