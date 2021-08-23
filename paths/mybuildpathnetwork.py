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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the path network as a list of lines between all path nodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = []
	### YOUR CODE GOES BELOW HERE ###
	firstO = []
	obsEdges = world.getLines()
	obsPoints = world.getPoints()
	maxRadius = agent.getMaxRadius()

	#potential line maker
	pt = []
	pt.append((pathnodes[0], pathnodes[len(pathnodes) - 1]))
	for value in pathnodes:
		for valueT in pathnodes:
			k = (value, valueT)
			m = (valueT, value)
			if k not in pt and m not in pt:
				pt.append(k)

	for lineM in pt:
		if rayTraceWorld(lineM[0], lineM[1], obsEdges) == None:
			lines.append(lineM)

	for pointer in lines:
		yuvanesh = True
		for point in obsPoints:
			if minimumDistance(pointer, point) < maxRadius:
				yuvanesh = False
		if yuvanesh == True:
			firstO.append(pointer)

	lines = firstO

	### YOUR CODE GOES ABOVE HERE ###
	return lines
