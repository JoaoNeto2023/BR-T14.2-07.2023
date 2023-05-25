from dino_runner.utils.constants import HEART
from dino_runner.utils.constants import DEFAULT_TYPE

from dino_runner.components.power_ups.power_up import PowerUp


class Small_heart(PowerUp):
    def __init__(self):
        #enviando a imagem do HEART e o tipo DEFAULT_TYPE
        super().__init__(image=HEART, type=DEFAULT_TYPE)
        
        