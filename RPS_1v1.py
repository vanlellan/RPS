#!/usr/bin/python3
#vanlellan/RPS/RPS_1v1.py: Testing implementation of sphere rotation for RPS battle mechanic
#Copyright 2023 Randall Evan McClellan

#This file is part of vanlellan/RPS.
#
#    vanlellan/RPS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    vanlellan/RPS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with vanlellan/RPS.  If not, see <http://www.gnu.org/licenses/>.

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

def drawSphere(aSphere, aP, aO):
	background = []
	foreground = []
	for i,p in enumerate(aSphere.points):
		x = aP.u[0]*p[0]+aP.u[1]*p[1]+aP.u[2]*p[2]
		y = aP.v[0]*p[0]+aP.v[1]*p[1]+aP.v[2]*p[2]
		z = aP.w[0]*p[0]+aP.w[1]*p[1]+aP.w[2]*p[2]
		if z >= 0.0:
			foreground.append((x,y,z)+tuple(50+0.25*x for x in aSphere.colors[i]))
		else:
			background.append((x,y,z)+tuple(50+0.25*x for x in aSphere.colors[i]))

	xSafe = (aP.u[0]+aP.u[1]+aP.u[2])/1.73
	ySafe = (aP.v[0]+aP.v[1]+aP.v[2])/1.73
	zSafe = (aP.w[0]+aP.w[1]+aP.w[2])/1.73
	if zSafe >= 0.0:
		foreground.append((xSafe,ySafe,zSafe,255,255,255))
		background.append((-xSafe,-ySafe,-zSafe,255,255,255))
	else:
		background.append((xSafe,ySafe,zSafe,255,255,255))
		foreground.append((-xSafe,-ySafe,-zSafe,255,255,255))

	g1 = (aO.w[2], aO.w[0], aO.w[1])
	g2 = (-aO.w[1], -aO.w[2], -aO.w[0])
	x1 = aP.u[0]*g1[0]+aP.u[1]*g1[1]+aP.u[2]*g1[2]
	y1 = aP.v[0]*g1[0]+aP.v[1]*g1[1]+aP.v[2]*g1[2]
	z1 = aP.w[0]*g1[0]+aP.w[1]*g1[1]+aP.w[2]*g1[2]
	x2 = aP.u[0]*g2[0]+aP.u[1]*g2[1]+aP.u[2]*g2[2]
	y2 = aP.v[0]*g2[0]+aP.v[1]*g2[1]+aP.v[2]*g2[2]
	z2 = aP.w[0]*g2[0]+aP.w[1]*g2[1]+aP.w[2]*g2[2]
	if z1 >= 0.0:
		foreground.append((x1,y1,z1)+GREEN)
		background.append((-x1,-y1,-z1)+RED)
	else:
		background.append((x1,y1,z1)+GREEN)
		foreground.append((-x1,-y1,-z1)+RED)
	if z2 >= 0.0:
		foreground.append((x2,y2,z2)+GREEN)
		background.append((-x2,-y2,-z2)+RED)
	else:
		background.append((x2,y2,z2)+GREEN)
		foreground.append((-x2,-y2,-z2)+RED)


	for p in background:
		pygame.draw.circle(DISPLAYSURF, p[3:], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(2.5*(p[2]+1.0)**2), 0)
	for p in foreground:
		pygame.draw.circle(DISPLAYSURF, p[3:], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(2.5*(p[2]+1.0)**2), 0)
	
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
			aPlayer1.rotate(aPlayer1.u, 1.0, aPlayer1.speed)
		if press[K_s]:
			aPlayer1.rotate(aPlayer1.u,-1.0, aPlayer1.speed)
		if press[K_d]:
			aPlayer1.rotate(aPlayer1.v, 1.0, aPlayer1.speed)
		if press[K_a]:
			aPlayer1.rotate(aPlayer1.v,-1.0, aPlayer1.speed)
		if press[K_q]:
			aPlayer1.rotate(aPlayer1.w, 1.0, aPlayer1.speed)
		if press[K_e]:
			aPlayer1.rotate(aPlayer1.w,-1.0, aPlayer1.speed)
		if press[K_i]:
			aPlayer2.rotate(aPlayer2.u, 1.0, aPlayer2.speed)
		if press[K_k]:
			aPlayer2.rotate(aPlayer2.u,-1.0, aPlayer2.speed)
		if press[K_l]:
			aPlayer2.rotate(aPlayer2.v, 1.0, aPlayer2.speed)
		if press[K_j]:
			aPlayer2.rotate(aPlayer2.v,-1.0, aPlayer2.speed)
		if press[K_u]:
			aPlayer2.rotate(aPlayer2.w, 1.0, aPlayer2.speed)
		if press[K_o]:
			aPlayer2.rotate(aPlayer2.w,-1.0, aPlayer2.speed)
		aPlayer1.calcColor()
		aPlayer2.calcColor()
		SCORE -= 1.0*attack(aPlayer1,aPlayer2)
		DISPLAYSURF.fill(BLACK)
		drawSphere(aSphere, aPlayer1, aPlayer2)
		drawSphere(aSphere, aPlayer2, aPlayer1)
		pygame.draw.circle(DISPLAYSURF, GREEN, (aPlayer1.centerX,700), 45, 5)
		pygame.draw.circle(DISPLAYSURF, GREEN, (aPlayer2.centerX,700), 45, 5)
		drawScore(SCORE,scoreColor)
		pygame.display.update()
		if SCORE > 300 or SCORE < -300:
			scoreColor = (0,255,0)
			drawScore(SCORE,scoreColor)
			pygame.display.update()
			time.sleep(2.0)
			aPlayer1.reset(1.0)
			aPlayer2.reset(-1.0)
			SCORE = 0.0
			scoreColor = (255,255,255)
		time.sleep(0.02)

player1 = RPSPlayer(300,400,1.0)
player2 = RPSPlayer(900,400,-1.0)
sphere1 = RPSSphere()
gameloop(sphere1,player1,player2)


