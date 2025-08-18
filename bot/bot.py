from sc2.bot_ai import BotAI
from sc2.data import Result

#from __future__ import annotations
from loguru import logger
from sc2 import maps
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId


class CompetitiveBot(BotAI):
    """Main bot class that handles the game logic."""
    
    def __init__(self):
        super().__init__()

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        await self.chat_send("glhf")
        self.client.game_step = 2
        return



    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """

        if (self.can_afford(UnitTypeId.DRONE)
            and self.supply_left > 0
            and self.larva):
                self.larva.random.train(UnitTypeId.DRONE)
                return
        

        if (self.can_afford(UnitTypeId.OVERLORD)
            and self.supply_left == 0
            and self.larva):
                self.larva.random.train(UnitTypeId.OVERLORD)
                return






        return #end of on_step function





    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        self.chat_send("gg")
        print("Game ended.")
