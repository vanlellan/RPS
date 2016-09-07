# Testing implementation of sphere rotation for RPS battle mechanic
# R Evan McClellan -- 2016-09-06
#
# To-Do:
#	flatten circles toward edge to reduce overlap artefact
#	implement 'angular momentum' and friction
#	add dummy 'opponent' and implement RPS comparison and win/loss status

import pygame, sys
from pygame.locals import *
import time
import random
import matplotlib.pyplot as plt
import subprocess
import numpy as np
import math as m
from RPSClasses import *

pygame.init()
subprocess.call(['speech-dispatcher'])

DISPLAYWIDTH = 1200
DISPLAYHEIGHT = 800

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
pygame.display.set_caption("RPS Test")


def drawSphere(aSphere, aP):
	DISPLAYSURF.fill(BLACK)
	for i,p in enumerate(aSphere.points):
		if (aP.w[0]*p[0]+aP.w[1]*p[1]+aP.w[2]*p[2]) >= 0.0:
			pygame.draw.circle(DISPLAYSURF, aSphere.colors[i], (int(200.0*(aP.u[0]*p[0]+aP.u[1]*p[1]+aP.u[2]*p[2]))+600,int(200.0*(aP.v[0]*p[0]+aP.v[1]*p[1]+aP.v[2]*p[2]))+400), 5, 3)

def gameloop(aSphere, aPlayer):
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					subprocess.call(['spd-say','shutting down'])
					pygame.quit()
					sys.exit()
		press = pygame.key.get_pressed()
		if press[K_i]:
			aPlayer.rotate(aPlayer.u, 1.0)
		if press[K_k]:
			aPlayer.rotate(aPlayer.u,-1.0)
		if press[K_l]:
			aPlayer.rotate(aPlayer.v, 1.0)
		if press[K_j]:
			aPlayer.rotate(aPlayer.v,-1.0)
		if press[K_u]:
			aPlayer.rotate(aPlayer.w, 1.0)
		if press[K_o]:
			aPlayer.rotate(aPlayer.w,-1.0)
		drawSphere(aSphere, aPlayer)
		pygame.display.update()
		time.sleep(0.02)

player1 = RPSPlayer()
sphere1 = RPSSphere()
gameloop(sphere1,player1)


