"""Constants used through the simulation."""

BOUNDS_WIDTH: int = 600
MAX_X: float = BOUNDS_WIDTH / 2
MIN_X: float = -MAX_X
VIEW_WIDTH: int = BOUNDS_WIDTH + 20

BOUNDS_HEIGHT: int = 600
MAX_Y: float = BOUNDS_HEIGHT / 2
MIN_Y: float = -MAX_Y
VIEW_HEIGHT: int = BOUNDS_HEIGHT + 20

CELL_RADIUS: int = 10
CELL_COUNT: int = 50
INITIAL_INFECTED: int = 3
INITIAL_IMMUNE: int = 1
CELL_SPEED: float = 10.0

VULNERABLE: int = 0
INFECTED: int = 1
IMMUNE: int = -1

RECOVERY_PERIOD: int = 120

COLLECT_FREQUENCY: int = 1

MASK_EFF: float = .65
PERCENT_MASK: float = .5
if not PERCENT_MASK == 0:
    MASK_FREQUENCY: int = round(CELL_COUNT / (CELL_COUNT * PERCENT_MASK))