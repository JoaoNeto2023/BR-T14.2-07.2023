
from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import SHIELD
from dino_runner.utils.constants import SHIELD_TYPE

class Shield(PowerUp):
    def __init__(self):
        super().__init__(image=SHIELD, type=SHIELD_TYPE)
        