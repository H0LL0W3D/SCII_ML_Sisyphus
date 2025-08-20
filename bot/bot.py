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
import numpy as np


# each strategy will be implemented into a stack, where depth
# suggests how late into the game it is to be implemented, and
# should thus drop the more surface level strategies.
# - STRATEGIES -
# 12 pool
# early ling rush
# baneling bust
# roach ravager push

# overlord drop
# roach hydra timing attack
# lurker rush
# muta harass
# swarm host harass
# corruptors + roaches

# ultralisk ling attack
# broodlord corruptor ball

# each procedure is a distinct atomic decision
# I want my bot to be making.
# - IMPORTANT PROCEDURES -
#expand
#drone + queen inject
#attack
#retreat
#harass
#defend
#upgrade + research
#scout




class CompetitiveBot(BotAI):
    """Main bot class that handles the game logic."""
    
    def __init__(self):
        super().__init__()
        self.start_buildorder = True
        #self.strat_stack = np.stack()
        self.army = []
        self.scouters = [] #list of scouters

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        await self.chat_send("glhf")
        self.client.game_step = 2


    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """
        self.scout()


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
                

        #produce overlords if supply cap'd
        if (self.supply_left == 0
            and self.larva 
            and self.can_afford(UnitTypeId.OVERLORD)
            and not self.already_pending(UnitTypeId.OVERLORD)):
            self.larva.random.train(UnitTypeId.OVERLORD)
            
        #if have 10+ zlings, attack
        if (self.units(UnitTypeId.ZERGLING).amount >= 10):
            self.attack([UnitTypeId.ZERGLING])

        return #end of on_step function


    #send all idle units of UnitTypeId in list attackers to attack
    def attack(self, attackers: list):
        for attack_group in attackers:
            if (self.units(attack_group).amount > 0):
                for attacker in self.units(attack_group).idle:
                    attacker.attack(self.enemy_structures.not_flying.random_or(self.enemy_start_locations[0]).position)
        return


    #operate all idle scouting units to "investigate" the map (assume for overlords)
    def scout(self):
        #generate random position to scout
        position = (np.random.randint(0,64), np.random.randint(0,64))
        for overlord in self.units(UnitTypeId.OVERLORD).idle:
            overlord.move(Point2(position))





    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        self.chat_send("gg")
        print("Game ended.")
