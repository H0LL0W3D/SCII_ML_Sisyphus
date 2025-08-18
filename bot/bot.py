from sc2.bot_ai import BotAI
from sc2.data import Result

#from __future__ import annotations
from loguru import logger
from sc2 import maps
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.unit import Unit
from sc2.units import Units
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2


class CompetitiveBot(BotAI):
    """Main bot class that handles the game logic."""
    
    def __init__(self):
        super().__init__()
        self.start_buildorder = True

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

        if (self.start_buildorder):
            #if have spawning pool, disable start_buildorder
            if (self.structures(UnitTypeId.SPAWNINGPOOL).amount > 0):
                self.start_buildorder = False
                return

            #if supply == 15, build spawning pool
            if (self.structures(UnitTypeId.SPAWNINGPOOL).amount + self.already_pending(UnitTypeId.SPAWNINGPOOL) == 0
            and self.supply_used == 15):
                if not self.can_afford(UnitTypeId.SPAWNINGPOOL):
                    return

                await self.build(
                    UnitTypeId.SPAWNINGPOOL,
                        near=self.townhalls.first.position.towards(self.game_info.map_center, 5))

            #build drones if available
            if (self.can_afford(UnitTypeId.DRONE)
                and self.supply_left > 1
                and self.larva):
                    self.larva.random.train(UnitTypeId.DRONE)
                    return
            
            #build overlords of 1 away from supply cap'd
            if (self.can_afford(UnitTypeId.OVERLORD)
                and self.supply_left <= 1
                and not self.already_pending(UnitTypeId.OVERLORD)
                and self.larva):
                    self.larva.random.train(UnitTypeId.OVERLORD)
                    return

            return

        #produce zerglings
        if (self.can_afford(UnitTypeId.ZERGLING)
            and self.supply_left > 0
            and self.larva):
                self.larva.random.train(UnitTypeId.ZERGLING)
                return

        #produce overlords if supply cap'd
        if (self.supply_left == 0
            and self.larva 
            and self.can_afford(UnitTypeId.OVERLORD)
            and not self.already_pending(UnitTypeId.OVERLORD)):
            self.larva.random.train(UnitTypeId.OVERLORD)
            return


        return #end of on_step function

    async def droning(self):
        pass




    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        self.chat_send("gg")
        print("Game ended.")
