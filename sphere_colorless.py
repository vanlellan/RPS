# Testing implementation of sphere rotation for RPS battle mechanic
# R Evan McClellan -- 2016-09-06
#
# To-Do:
#	implement 'angular momentum' and friction
#DONE	implement RPS comparison and win/loss status (tug-of-war, cumulative continuous win/loss)
#DONE	add player 2, add "opponent" color swatch above each player sphere
#	move keybindings to player class
#DONE	make circles smaller toward horizon
#	make simple 'snaking' AI
#	make colorless version: draw win-maximization and loss-maximization points on the sphere itself


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
pygame.display.set_caption("TUG OF WAR")

def attack(aP1, aP2):
	#P1 attacks P2
	result = aP1.w[0]*(aP2.w[2]-aP2.w[1]) + aP1.w[1]*(aP2.w[0]-aP2.w[2]) + aP1.w[2]*(aP2.w[1]-aP2.w[0])
	return result

def drawScore(aScore, aColor):
	pygame.draw.circle(DISPLAYSURF, aColor, (DISPLAYWIDTH/2+int(aScore),700), 40, 0)

def drawSwatch(aPlayer, aOpponent):
#	pygame.draw.circle(DISPLAYSURF, aOpponent.color, (aPlayer.centerX,aPlayer.centerY-300), 40, 0)
#	pygame.draw.circle(DISPLAYSURF, (aOpponent.color[2],aOpponent.color[0],aOpponent.color[1]), (aPlayer.centerX-50,aPlayer.centerY-250), 10, 0)
#	pygame.draw.circle(DISPLAYSURF, (255.-aOpponent.color[1],255.-aOpponent.color[2],255.-aOpponent.color[0]), (aPlayer.centerX+50,aPlayer.centerY-250), 10, 0)
	g1 = (aOpponent.w[2], aOpponent.w[0], aOpponent.w[1])
	g2 = (-aOpponent.w[1], -aOpponent.w[2], -aOpponent.w[0])
	x1 = aPlayer.u[0]*g1[0]+aPlayer.u[1]*g1[1]+aPlayer.u[2]*g1[2]
	y1 = aPlayer.v[0]*g1[0]+aPlayer.v[1]*g1[1]+aPlayer.v[2]*g1[2]
	z1 = aPlayer.w[0]*g1[0]+aPlayer.w[1]*g1[1]+aPlayer.w[2]*g1[2]
	x2 = aPlayer.u[0]*g2[0]+aPlayer.u[1]*g2[1]+aPlayer.u[2]*g2[2]
	y2 = aPlayer.v[0]*g2[0]+aPlayer.v[1]*g2[1]+aPlayer.v[2]*g2[2]
	z2 = aPlayer.w[0]*g2[0]+aPlayer.w[1]*g2[1]+aPlayer.w[2]*g2[2]
	if z1 >= 0.0:
		pygame.draw.circle(DISPLAYSURF, GREEN, (int(200.0*x1+aPlayer.centerX),int(200.0*y1+aPlayer.centerY)), 10, 0)
	else:
		pygame.draw.circle(DISPLAYSURF, RED, (int(-200.0*x1+aPlayer.centerX),int(-200.0*y1+aPlayer.centerY)), 10, 0)
	if z2 >= 0.0:
		pygame.draw.circle(DISPLAYSURF, GREEN, (int(200.0*x2+aPlayer.centerX),int(200.0*y2+aPlayer.centerY)), 10, 0)
	else:
		pygame.draw.circle(DISPLAYSURF, RED, (int(-200.0*x2+aPlayer.centerX),int(-200.0*y2+aPlayer.centerY)), 10, 0)

def drawSphere(aSphere, aP):
	for i,p in enumerate(aSphere.points):
		z = aP.w[0]*p[0]+aP.w[1]*p[1]+aP.w[2]*p[2]
		if z >= 0.0:
			x = aP.u[0]*p[0]+aP.u[1]*p[1]+aP.u[2]*p[2]
			y = aP.v[0]*p[0]+aP.v[1]*p[1]+aP.v[2]*p[2]
			r = m.sqrt(x**2.0+y**2.0)
			pygame.draw.circle(DISPLAYSURF, GRAY, (int(200.0*x+aP.centerX),int(200.0*y+aP.centerY)), int(10*(1.0-(r*r/2.0))), 0)
	pygame.draw.circle(DISPLAYSURF, (255.-aP.color[0],255.-aP.color[1],255.-aP.color[2]), (aP.centerX,aP.centerY), 12, 2)
	xSafe = (aP.u[0]+aP.u[1]+aP.u[2])/1.73
	ySafe = (aP.v[0]+aP.v[1]+aP.v[2])/1.73
	rSafe = m.sqrt(xSafe**2.0+ySafe**2.0)
	zSafe = (aP.w[0]+aP.w[1]+aP.w[2])/1.73
	if zSafe >= 0.0:
		pygame.draw.circle(DISPLAYSURF, (150,150,150), (int(200.0*(xSafe)+aP.centerX),int(200.0*(ySafe)+aP.centerY)), int(10*(1.0-(rSafe*rSafe/2.0))), 0)
	else:
		pygame.draw.circle(DISPLAYSURF, (150,150,150), (int(200.0*(-xSafe)+aP.centerX),int(200.0*(-ySafe)+aP.centerY)), int(10*(1.0-(rSafe*rSafe/2.0))), 0)


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
		pygame.draw.circle(DISPLAYSURF, GREEN, (aPlayer1.centerX,700), 45, 5)
		pygame.draw.circle(DISPLAYSURF, GREEN, (aPlayer2.centerX,700), 45, 5)
		drawScore(SCORE,scoreColor)
		pygame.display.update()
		if SCORE > 300 or SCORE < -300:
			scoreColor = (0,255,0)
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

