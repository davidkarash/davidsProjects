"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730407523"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Determine the distance between two Point objects."""
        dx: float = self.x - other.x
        dy: float = self.y - other.y
        return sqrt((dx ** 2) + (dy ** 2))


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE
    mask: bool = False

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    def tick(self) -> None:
        """Updates cell attributes and location."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness += 1
        if self.sickness >= constants.RECOVERY_PERIOD:
            self.immunize()
        
    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable():
            return "gray"
        if self.is_infected():
            return "red"
        if self.is_immune():
            return "light sky blue"
        return "gray"

    def contract_disease(self) -> None:
        """Makes a cell infected."""
        if self.is_vulnerable():
            self.sickness = constants.INFECTED
    
    def is_vulnerable(self) -> bool:
        """Checks if a cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        return False
    
    def is_infected(self) -> bool:
        """Checks if a cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True
        return False

    def contact_with(self, other: Cell) -> None:
        """Infects cells if they make contact and are vulnerable."""
        if self.is_infected() or other.is_infected():

            if self.is_vulnerable():
                if self.mask:
                    if random() > constants.MASK_EFF:
                        self.contract_disease()
                else:
                    self.contract_disease()

            if other.is_vulnerable():
                if other.mask:
                    if random() > constants.MASK_EFF:
                        other.contract_disease()
                else:
                    other.contract_disease()
    
    def immunize(self) -> None:
        """Makes a cell immune."""
        self.sickness = constants.IMMUNE
        
    def is_immune(self) -> bool:
        """Checks to see if a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        return False


class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, t0_infected: int, t0_immune: int = 0):
        """Initialize the cells with random locations and directions."""
        # Check for errors
        found_error: bool = False
        if t0_infected + t0_immune >= cells:
            found_error = True
        elif t0_infected <= 0 or t0_immune < 0:
            found_error = True
        if found_error:
            raise ValueError("Some cells must be vulnerable and some must be infected.")
        self.population = []
        for i in range(0, cells):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            if i < t0_infected:
                self.population.append(Cell(start_loc, start_dir))
                self.population[i].sickness = constants.INFECTED
            elif i < t0_infected + t0_immune:
                self.population.append(Cell(start_loc, start_dir))
                self.population[i].sickness = constants.IMMUNE
            else:
                self.population.append(Cell(start_loc, start_dir))
            if not constants.PERCENT_MASK == 0:
                if i % constants.MASK_FREQUENCY == 0:
                    self.population[i].mask = True
    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def check_contacts(self) -> None:
        """Checks to see which cells make contact."""
        i: int = 0
        d: float
        while i < len(self.population):
            for j in range(i + 1, len(self.population)):
                d = self.population[i].location.distance(self.population[j].location)
                if d < constants.CELL_RADIUS:
                    self.population[i].contact_with(self.population[j])
            i += 1
        return None

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for cell in self.population:
            if cell.is_infected():
                return False
        return True