"""Hypothesis: Increasing the area availible will decrease infections.

Increasing the area is similar to moving an in person event
outdoors in order to reduce the chance of infections.

RESULT: Doubling the simulation area significantly reduces the amount of individuals
who become infected by a factor of around 1/2.
"""


from projects.pj02 import constants
from projects.pj02.model import Model
from typing import List
import argparse

parser = argparse.ArgumentParser("Chart a viral simulation.")
parser.add_argument("-c", "--cellcount", type=int, help="input number of total cells.")
parser.add_argument("-inf", "--init_infected", type=int, help="input initial infected cells.")
parser.add_argument("-im", "--immune", type=int, help="input initial number of immune cells.")
args = parser.parse_args()
initial_cells: int
initial_inf: int
initial_immune: int
if args.cellcount:
    initial_cells = args.cellcount
else:
    initial_cells = constants.CELL_COUNT
if args.init_infected:
    initial_inf = args.init_infected
else:
    initial_inf = constants.INITIAL_INFECTED
if args.immune:
    initial_immune = args.immune
else:
    initial_immune = constants.INITIAL_IMMUNE


class ModelState:
    time: int
    vulnerable: int
    infected: int
    immune: int

    def __init__(self, model: Model):
        """Creates ModelState."""
        self.time = model.time
        count_v: int = 0
        count_inf: int = 0
        count_immune: int = 0
        for cell in model.population:
            if cell.is_vulnerable():
                count_v += 1
            elif cell.is_infected():
                count_inf += 1
            elif cell.is_immune():
                count_immune += 1
        self.vulnerable = count_v
        self.infected = count_inf
        self.immune = count_immune
    

def main() -> None:
    model = Model(initial_cells, constants.CELL_SPEED, initial_inf, initial_immune)
    data: List[ModelState] = []
    while not model.is_complete():
        model.tick()
        if model.time % constants.COLLECT_FREQUENCY == 0:
            data.append(collect_data(model))
    data.append(collect_data(model))
    chart(data)
    return None


def collect_data(model: Model) -> ModelState:
    data = ModelState(model)
    return data


def chart(data: List[ModelState]) -> None:
    # Create Lists from data
    times: List[int] = []
    infected: List[int] = []
    immune: List[int] = []
    vulnerable: List[int] = []
    for state in data:
        times.append(state.time)
        infected.append(state.infected)
        immune.append(state.immune)
        vulnerable.append(state.vulnerable)
    # Plot lists
    import matplotlib.pyplot as plt
    plt.title(f"Initial Infected: {constants.INITIAL_INFECTED}    Initial Immune: {constants.INITIAL_IMMUNE}\
        Total Cells: {constants.CELL_COUNT}   Area: {constants.MAX_X * 4 * constants.MAX_Y}")
    plt.plot(times, infected, "red")
    plt.plot(times, immune, "blue")
    plt.plot(times, vulnerable, "gray")
    plt.xlabel("Time")
    plt.ylabel("Number of Cells")
    plt.show()


if __name__ == "__main__":
    main()