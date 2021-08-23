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



###############################
### AStarNavigator2
###
### Creates a path node network and implements the A* algorithm to create a path to the given destination.
			
class AStarNavigator2(PathNetworkNavigator):

				
	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., its current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		self.setPath(None)
		### Make sure the next and dist matrices exist
		if self.agent != None and self.world != None: 
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			### Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			### Tell the agent to move to dest
			if clearShot(source, dest, self.world.getLinesWithoutBorders(), self.world.getPoints(), self.agent):
				self.agent.moveToTarget(dest)
			else:
				### Step 2: If there is an obstacle, create the path that will move around the obstacles.
				### Find the path nodes closest to source and destination.
				start = getOnPathNetwork(source, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				end = getOnPathNetwork(dest, self.pathnodes, self.world.getLinesWithoutBorders(), self.agent)
				if start != None and end != None:
					### Remove edges from the path network that intersect gates
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates(), self.world)
					closedlist = []
					### Create the path by traversing the pathnode network until the path node closest to the destination is reached
					path, closedlist = astar(start, end, newnetwork)
					if path is not None and len(path) > 0:
						### Determine whether shortcuts are available
						path = shortcutPath(source, dest, path, self.world, self.agent)
						### Store the path by calling self.setPath()
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							### Tell the agent to move to the first node in the path (and pop the first node off the path)
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None
		
	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcuts can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

	def update(self, delta):
		myUpdate(self, delta)


### Removes any edge in the path network that intersects a worldLine (which should include gates).
def unobstructedNetwork(network, worldLines, world):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork



### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
	### YOUR CODE GOES BELOW HERE ###
	bob = True
	if rayTraceWorld(p1, p2, worldLines) != None:
		return False
	for point in worldPoints:
		if distance(p1, point) + distance(p2, point) == distance(p1, p2):
			return False
	return True

	### YOUR CODE GOES ABOVE HERE ###
	return False

### Given a location, find the closest pathnode that the agent can get to without collision
### agent: the agent
### location: the location to check from (typically where the agent is starting from or where the agent wants to go to) as an (x, y) point
### pathnodes: a list of pathnodes, where each pathnode is an (x, y) point
### world: pointer to the world
def getOnPathNetwork(location, pathnodes, worldLines, agent):
	node = None
	### YOUR CODE GOES BELOW HERE ###

	adam = {}
	for node in pathnodes:
		if clearShot(location, node, worldLines, [], agent):
			adam[distance(location, node)] = node
	yuvan = min(list(adam.keys()))
	node = adam[yuvan]

	### YOUR CODE GOES ABOVE HERE ###
	return node



### Implement the a-star algorithm
### Given:
### Init: a pathnode (x, y) that is part of the pathnode network
### goal: a pathnode (x, y) that is part of the pathnode network
### network: the pathnode network
### Return two values: 
### 1. the path, which is a list of states that are connected in the path network
### 2. the closed list, the list of pathnodes visited during the search process
def astar(init, goal, network):
	path = []
	open = []
	closed = []
	### YOUR CODE GOES BELOW HERE ###

	graph = {}
	for line in network:
		if line[0] not in graph.keys():
			graph[line[0]] = [line[1]]
		else:
			graph[line[0]].append(line[1])
		if line[1] not in graph.keys():
			graph[line[1]] = [line[0]]
		else:
			graph[line[1]].append(line[0])

	start = init
	open.append(start)
	storage = {}
	for marker in graph.keys():
		storage[marker] = {'h' : distance(marker, goal), 'g' : 0, 'parent' : None}

	# storage[start] = {'h': distance(start, goal), 'g': 0, 'parent': None}
	# storage[goal] = {'h': 0, 'g': 0, 'parent': None}

	while len(open) > 0:
			current = open[0]
			currentInd = 0
			for index, item in enumerate(open):
				if storage[item]['h'] + storage[item]['g'] < storage[current]['h'] + storage[current]['g']:
					current = item
					currentInd = index
			open.pop(currentInd)
			if current == goal:
				markX = current
				while markX is not None:
					path.append(markX)
					markX = storage[markX]['parent']
				path = path[::-1]
				return path, closed

			if current not in closed:
				closed.append(current)

				children = graph[current]
				for child in children:
					# for secChild in closed:
					# 	if child == secChild:
					# 		continue

					# storage[child]['g'] = storage[current]['g'] + distance(child, current)
					# storage[child]['parent'] = current
					if child not in closed:
						storage[child] = {'h': distance(start, goal), 'g': storage[current]['g'] + distance(child, current), 'parent': current}
						open.append(child)
					# for bLNode in open:
					# 	if child == bLNode and storage[child]['g'] < storage[bLNode]['g']:
					# 		open.append(child)



	### YOUR CODE GOES ABOVE HERE ###
	return path, closed




def myUpdate(nav, delta):
	### YOUR CODE GOES BELOW HERE ###
	myCheckpoint(nav)

	### YOUR CODE GOES ABOVE HERE ###
	return None

def myCheckpoint(nav):
	### YOUR CODE GOES BELOW HERE ###
	yuvanP = nav.agent.getLocation()
	Sarah = nav.agent.getMoveTarget()
	Kiran = nav.world.getLinesWithoutBorders()
	Josh = nav.world.getPoints()
	Podrick = nav.agent

	currentLocation = nav.agent.getLocation()
	goalLocation = nav.getDestination()

	if not clearShot(yuvanP, Sarah, Kiran, Josh, Podrick) and nav.getDestination():
		nav.computePath(currentLocation, goalLocation)
		if nav.getPath() == False:
			nav.agent.stopMoving()

	### YOUR CODE GOES ABOVE HERE ###
	return None

### This function optimizes the given path and returns a new path
### source: the current position of the agent
### dest: the desired destination of the agent
### path: the path previously computed by the A* algorithm
### world: pointer to the world
def shortcutPath(source, dest, path, world, agent):
	path = copy.deepcopy(path)
	### YOUR CODE GOES BELOW HERE ###

	path2, start = copy.deepcopy(path), source
	path.append(dest)
	path2.append(dest)
	for i in range(0, len(path2) - 1):
		current, next = path2[i], path2[i + 1]
		if clearShot(start, next, world.getLines(), world.getPoints(), agent):
			path.remove(current)
		else:
			start = current
	path.remove(dest)

	### YOUR CODE GOES BELOW HERE ###
	return path


### This function changes the move target of the agent if there is an opportunity to walk a shorter path.
### This function should call nav.agent.moveToTarget() if an opportunity exists and may also need to modify nav.path.
### nav: the navigator object
### This function returns True if the moveTarget and/or path is modified and False otherwise
def mySmooth(nav):
	### YOUR CODE GOES BELOW HERE ###

	current = nav.agent.getLocation()
	theLines = nav.world.getLinesWithoutBorders()
	thePoints = nav.world.getPoints()
	theAgent = nav.agent

	goalLocation = nav.getDestination()
	thePath = nav.getPath()

	if clearShot(current, goalLocation, theLines, thePoints, theAgent):
		nav.path = []
		nav.agent.moveToTarget(goalLocation)
		return True

	if clearShot(current, thePath[1], theLines, thePoints, theAgent):
		nav.path.remove[thePath[0]]
		nav.agent.moveToTarget(thePath[1])
		return True

	### YOUR CODE GOES ABOVE HERE ###
	return False

