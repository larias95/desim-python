# DeSim (Discrete Event Simulator)

A Discrete Event Simulation (DES) framework for modeling systems where state changes occur at discrete points in time.

## Description

*to be added*

### Features

- 📦 OOP: Object-oriented paradigm was taken in mind in order to allow flexibility while modeling dynamic systems.
- ⏱️ Discrete time: Time updates are based on occurrences of events, and not on delta times.
- ⏩ Queue-based: Events are retrieved from a priority queue that sorts them based on their time of occurrence.
- 🍃 Lightweight: DeSim has no external dependencies.

### Quick Example

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
