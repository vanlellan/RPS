# Testing implementation of sphere rotation for RPS battle mechanic
# R Evan McClellan -- 2016-09-06
#
# To-Do:
#	flatten circles toward edge to reduce overlap artefact
#	implement 'angular momentum' and friction
#	implement RPS comparison and win/loss status (tug-of-war, cumulative continuous win/loss)
#DONE	add player 2, add "opponent" color swatch above each player sphere
#	move keybindings to player class
#	make circles smaller toward horizon

import pygame, sys
from pygame.locals import *
import time
import math as m
from RPSClasses import *

pygame.init()

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

def attack(aP1, aP2):
	#P1 attacks P2
	result = aP1.w[0]*(aP2.w[2]-aP2.w[1]) + aP1.w[1]*(aP2.w[0]-aP2.w[2]) + aP1.w[2]*(aP2.w[1]-aP2.w[0])
	return result

def drawScore(aScore, aColor):
	pygame.draw.circle(DISPLAYSURF, aColor, (DISPLAYWIDTH/2+int(aScore),700), 40, 0)

def drawSwatch(aPlayer, aOpponent):
	pygame.draw.circle(DISPLAYSURF, aOpponent.color, (aPlayer.centerX,aPlayer.centerY-300), 40, 0)
	pygame.draw.circle(DISPLAYSURF, (aOpponent.color[1],aOpponent.color[2],aOpponent.color[0]), (aPlayer.centerX-50,aPlayer.centerY-250), 10, 0)
	pygame.draw.circle(DISPLAYSURF, (255.-aOpponent.color[2],255.-aOpponent.color[0],255.-aOpponent.color[1]), (aPlayer.centerX+50,aPlayer.centerY-250), 10, 0)

def drawSphere(aSphere, aP):
	for i,p in enumerate(aSphere.points):
		if (aP.w[0]*p[0]+aP.w[1]*p[1]+aP.w[2]*p[2]) >= 0.0:
			pygame.draw.circle(DISPLAYSURF, aSphere.colors[i], (int(200.0*(aP.u[0]*p[0]+aP.u[1]*p[1]+aP.u[2]*p[2]))+aP.centerX,int(200.0*(aP.v[0]*p[0]+aP.v[1]*p[1]+aP.v[2]*p[2]))+aP.centerY), 10, 0)
	pygame.draw.circle(DISPLAYSURF, (255.-aP.color[0],255.-aP.color[1],255.-aP.color[2]), (aP.centerX,aP.centerY), 12, 2)


def gameloop(aSphere, aPlayer1, aPlayer2):
	SCORE = 0.0
	scoreColor = (255,255,255)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
		press = pygame.key.get_pressed()
		if press[K_w]:
			aPlayer1.rotate(aPlayer1.u, 1.0)
		if press[K_s]:
			aPlayer1.rotate(aPlayer1.u,-1.0)
		if press[K_d]:
			aPlayer1.rotate(aPlayer1.v, 1.0)
		if press[K_a]:
			aPlayer1.rotate(aPlayer1.v,-1.0)
		if press[K_q]:
			aPlayer1.rotate(aPlayer1.w, 1.0)
		if press[K_e]:
			aPlayer1.rotate(aPlayer1.w,-1.0)
		if press[K_i]:
			aPlayer2.rotate(aPlayer2.u, 1.0)
		if press[K_k]:
			aPlayer2.rotate(aPlayer2.u,-1.0)
		if press[K_l]:
			aPlayer2.rotate(aPlayer2.v, 1.0)
		if press[K_j]:
			aPlayer2.rotate(aPlayer2.v,-1.0)
		if press[K_u]:
			aPlayer2.rotate(aPlayer2.w, 1.0)
		if press[K_o]:
			aPlayer2.rotate(aPlayer2.w,-1.0)
		aPlayer1.calcColor()
		aPlayer2.calcColor()
		SCORE -= 1.0*attack(aPlayer1,aPlayer2)
		DISPLAYSURF.fill(BLACK)
		drawSphere(aSphere, aPlayer1)
		drawSphere(aSphere, aPlayer2)
		drawSwatch(aPlayer1, aPlayer2)
		drawSwatch(aPlayer2, aPlayer1)
		pygame.draw.circle(DISPLAYSURF, RED, (aPlayer1.centerX,700), 45, 5)
		pygame.draw.circle(DISPLAYSURF, RED, (aPlayer2.centerX,700), 45, 5)
		drawScore(SCORE,scoreColor)
		pygame.display.update()
		if SCORE > 300 or SCORE < -300:
			scoreColor = (255,0,0)
			drawScore(SCORE,scoreColor)
			pygame.display.update()
			time.sleep(2.0)
			aPlayer1.reset()
			aPlayer2.reset()
			SCORE = 0.0
			scoreColor = (255,255,255)
		time.sleep(0.02)

player1 = RPSPlayer(300,400)
player2 = RPSPlayer(900,400)
sphere1 = RPSSphere()
gameloop(sphere1,player1,player2)


