# A implementation of Conway's Game of Live on a hexagonal grid
# to practice calcuations and graphics with hexagonal grids
#
# R Evan McClellan -- 2016-07-24

import pygame, sys
from pygame.locals import *
import time
import random
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import math as m

pygame.init()
subprocess.call(['speech-dispatcher'])

DISPLAYWIDTH = 1200
DISPLAYHEIGHT = 800

SCALEFACTOR = 10

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GRAY  = (100, 100, 100)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
YELLOW= (255, 255, 100)

# set up the window
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), 0, 32)
pygame.display.set_caption('RPS Mechanic Proof of Concept')

WORLDTENSOR = np.array(((0,-1,1),(1,0,-1),(-1,1,0)))

class player():
#player class, holds current RPS state and whatever
	def __init__(self):
		self.radius = 1.0
		self.theta = 1.5
		self.phi = 1.5
		self.rock =     self.radius * m.cos(self.theta) * m.sin(self.phi)
		self.paper =    self.radius * m.sin(self.theta) * m.sin(self.phi)
		self.scissors = self.radius * m.cos(self.phi)

	def calc_rps(self):
		self.rock =     self.radius * m.cos(self.theta) * m.sin(self.phi)
		self.paper =    self.radius * m.sin(self.theta) * m.sin(self.phi)
		self.scissors = self.radius * m.cos(self.phi)

	def attack(self, aOther):
		attackerT = np.array((self.rock, self.paper, self.scissors))
		defender = np.array((aOther.rock, aOther.paper, aOther.scissors)).reshape(3,1)
#		print defenderT, WORLDTENSOR, attacker
		preResult = np.dot(WORLDTENSOR,defender)
		result = np.dot(attackerT, preResult)
		return result

def drawCircle(color, size, x, y):
	pygame.draw.circle(DISPLAYSURF, color, (x,y), size, 0)


def gameloop(aP1,aP2):
	outcome = 0.0
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
#			elif event.type == MOUSEMOTION:
#				xcur, ycur = event.pos
#				cursor = getCellFromCursor(xcur,ycur)
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					subprocess.call(['spd-say','shutting down'])
					pygame.quit()
					sys.exit()
				elif event.key == K_i:
					aP1.theta += 0.1
				elif event.key == K_k:
					aP1.theta -= 0.1
				elif event.key == K_j:
					aP1.phi += 0.1
				elif event.key == K_l:
					aP1.phi -= 0.1
				elif event.key == K_a or event.key == K_RETURN:
					outcome = aP1.attack(aP2)
					if outcome > 0.0:
						subprocess.call(['spd-say','victorious'])
					if outcome < 0.0:
						subprocess.call(['spd-say','defeated'])
					print "Outcome: ", outcome
		outcomeI = int(10.0*abs(outcome))
		aP1.calc_rps()
		rockI = int(20.0*abs(aP1.rock))
		paperI = int(20.0*abs(aP1.paper))
		scissorsI = int(20.0*abs(aP1.scissors))
		rockI2 = int(20.0*abs(aP2.rock))
		paperI2 = int(20.0*abs(aP2.paper))
		scissorsI2 = int(20.0*abs(aP2.scissors))
#		print rockI, paperI, scissorsI
		DISPLAYSURF.fill(BLACK)
		basicfont = pygame.font.SysFont(None, 48)
		textR = basicfont.render(str(aP1.rock), True, WHITE)
		textP = basicfont.render(str(aP1.paper), True, WHITE)
		textS = basicfont.render(str(aP1.scissors), True, WHITE)
		rectR = textR.get_rect()
		rectP = textP.get_rect()
		rectS = textS.get_rect()
		rectR.centerx = 300
		rectR.centery = 700
		rectP.centerx = 600
		rectP.centery = 700
		rectS.centerx = 900
		rectS.centery = 700
		DISPLAYSURF.blit(textR, rectR)
		DISPLAYSURF.blit(textP, rectP)
		DISPLAYSURF.blit(textS, rectS)
		if aP1.rock>=0:
			drawCircle(GREEN,rockI,300,600)
		else:
			drawCircle(RED,rockI,300,600)
		if aP1.paper>=0:
			drawCircle(GREEN,paperI,600,600)
		else:
			drawCircle(RED,paperI,600,600)
		if aP1.scissors>=0:
			drawCircle(GREEN,scissorsI,900,600)
		else:
			drawCircle(RED,scissorsI,900,600)
		if aP2.rock>=0:
			drawCircle(GREEN,rockI2,300,200)
		else:
			drawCircle(RED,rockI2,300,200)
		if aP2.paper>=0:
			drawCircle(GREEN,paperI2,600,200)
		else:
			drawCircle(RED,paperI2,600,200)
		if aP2.scissors>=0:
			drawCircle(GREEN,scissorsI2,900,200)
		else:
			drawCircle(RED,scissorsI2,900,200)
		if outcome>=0:
			drawCircle(GREEN,outcomeI,600,400)
		else:
			drawCircle(RED,outcomeI,600,400)
		pygame.display.update()
		time.sleep(0.1)

print WORLDTENSOR
print "Notes:"
print "\t-Three circles along the bottom are your 'rockness', 'paperness', and 'scissorsness'"
print "\t-Green positive, red is negative (i.e. there is such thing as 'antirock')"
print "\t-The size of the circles indicates magnitude"
print "\t-They are normalized, such that (rock)^2 + (paper)^2 + (scissors)^2 = 1"
print "\t-Use ijkl to rotate your RPS vector\n"
print "\t-The upper circles are the 'AI' player (static for now)"
print "\t-You can attack by pressing 'a' or 'enter'"
print "\t-Attacking updates the circle in the middle"
print "\t-Grean means you win, red means you lose"
print "\t-Again, size indicates the magnitude of the win or loss"
p1 = player()
p2 = player()
gameloop(p1,p2)


