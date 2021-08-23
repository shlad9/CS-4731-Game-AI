
'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *
from moba import *


class MyMinion(Minion):

	def __init__(self, position, orientation, world, image=NPC, speed=SPEED, viewangle=360, hitpoints=HITPOINTS,
				 firerate=FIRERATE, bulletclass=SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle, Defensive, Attack, TowerHunt]
		### Add your states to self.states (but don't remove Idle)
		### YOUR CODE GOES BELOW HERE ###
		ident = numpy.random.choice(numpy.arange(1, 10), p=[0, 0, 0, 0, 0, 0, 0.2, 0, 0.8])
		# if ident is greater than or equal to 6 will make it go for the towers
		# when it is 5 or less, it will make it in charge of attacking other minions
		if ident >= 6:
			self.motive = False  # "TOWER"
		else:
			self.motive = True  # Minion

	### YOUR CODE GOES ABOVE HERE ###

	def start(self):
		Minion.start(self)
		self.changeState(Idle)


############################
## Idle
##
## This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):

	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()

	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		if len(self.agent.world.getEnemyTowers(self.agent.getTeam())) == 0:
			bases = self.agent.world.getEnemyBases(self.agent.getTeam())
			self.agent.changeState(TowerHunt, bases[0].getLocation(), bases[0])
		if self.agent.motive:
			myTows = self.agent.world.getTowersForTeam(self)
			myTows = sorted(myTows, key=(lambda x: distance(x.getLocation(), self.agent.getLocation())))
			if len(myTows) > 0:
				self.agent.changeState(Defensive, myTows[0])
		else:
			tows = self.agent.world.getEnemyTowers(self.agent.getTeam())
			tows = sorted(tows, key=(lambda x: distance(x.getLocation(), self.agent.getLocation())))
			tows = tows + self.agent.world.getEnemyBases(self.agent.getTeam())
			if len(tows) > 0:
				self.agent.changeState(TowerHunt, tows[0].getLocation(), tows[0])

		### YOUR CODE GOES ABOVE HERE ###
		return None
#
# ##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print("Hey " + str(self.victim) + ", I don't like you!")
		self.agent.changeState(Idle)
#
# ##############################
### YOUR STATES GO HERE:

class Attack(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		State.execute(self, delta)
		if self.victim is not None:
			self.agent.turnToFace(self.victim.position)
			self.agent.shoot()
		if self.victim.isAlive():
			self.agent.changeState(Attack, self.victim)
		else:
			self.agent.changeState(Idle)

class TowerHunt(State):

	def parseArgs(self, args):
		self.destination = args[0] #tower location
		self.tower = args[1] #the tower itself
	def enter(self, oldstate):
		State.enter(self, oldstate)
		if self.tower is not None:
			self.agent.navigateTo(self.destination)
	def execute(self, delta = 0):
		State.execute(self, delta)
		if distance(self.agent.position, self.destination) < SMALLBULLETRANGE:
			self.agent.stopMoving()
			self.agent.changeState(Attack, self.tower)
		else:
			self.agent.navigateTo(self.destination)

class Defensive(State):
	def parseArgs(self, args):
		self.defend = args[0]
		self.destin = args[0].getLocation()
	def enter(self, oldstate):
		if oldstate == Idle:
			agent.naviageTo(self.destin)
	def exectute(self, delta = 0):
		if self.agent.position() == self.agent.destin:
			self.agent.stopMoving()
			enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
			for enemy in enemies:
				if util.distance(enemy.position, self.agent.position) <= SMALLBULLETRANGE:
					self.agent.changeState(Attack, enemy)