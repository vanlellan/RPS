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

def rotate3Vector(wIn,axis,theta):
	a = m.cos(theta/2.0)
	b = m.sin(theta/2.0)
	q = Quaternion(a, axis[0]*b, axis[1]*b, axis[2]*b)
	wQ = Quaternion(0.0, wIn[0], wIn[1], wIn[2])
	q.conjugate()
	wQ.multL(q)
	q.conjugate()
	wQ.multR(q)
	return (wQ.comp[1], wQ.comp[2], wQ.comp[3])

def attack(aP1, aP2):
	#P1 attacks P2
	result = aP1.w[0]*(aP2.w[2]-aP2.w[1]) + aP1.w[1]*(aP2.w[0]-aP2.w[2]) + aP1.w[2]*(aP2.w[1]-aP2.w[0])
	return result

def attack4D(a, b):
	#a attacks b in FOUR DIMENSIONS (use 1.4 for sqrt(2))
	A0 =  a[0]*0.0 + a[1]/1.4 + a[2]/2.0
	A1 =  a[0]/1.4 + a[1]*0.0 - a[2]/2.0
	A2 =  a[0]*0.0 - a[1]/1.4 + a[2]/2.0
	A3 = -a[0]/1.4 + a[1]*0.0 - a[2]/2.0
	B0 =  b[0]*0.0 + b[1]/1.4 + b[2]/2.0
	B1 =  b[0]/1.4 + b[1]*0.0 - b[2]/2.0
	B2 =  b[0]*0.0 - b[1]/1.4 + b[2]/2.0
	B3 = -b[0]/1.4 + b[1]*0.0 - b[2]/2.0
	#result = A0*(B3-B1) + A1*(B0-B2) + A2*(B1-B3) + A3*(B2-B0)	#	M = [[0,-1,0,1][1,0,-1,0][0,1,0,-1][-1,0,1,0]]
	result = A0*(B2-B1) + A1*(B3-B2) + A2*(B0-B3) + A3*(B1-B0)	#	M = [[0,-1,1,0][0,0,-1,1][1,0,0,-1][-1,1,0,0]]
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
		r = 1.0# - 0.5*abs(p[0]/m.sqrt(3)+p[1]/m.sqrt(3)+p[2]/m.sqrt(3))
		comp = attack4D(p,aO.w)
		#comp = attack2(p,aO.w)
		if z >= 0.0:
		#	foreground.append((r*x,r*y,r*z)+tuple(50+0.25*x for x in aSphere.colors[i])+(0.5,))
		#	foreground.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(0.5*a*abs(comp)))) for a in aSphere.colors[i])+(1.0,))
			if comp > 0.0:
				foreground.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(0.5*a*comp))) for a in GREEN)+(0.5,))
			else:
				foreground.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(-0.5*a*comp))) for a in RED)+(0.5,))
		else:
			if comp > 0.0:
				background.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(0.5*a*comp))) for a in GREEN)+(0.5,))
			else:
				background.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(-0.5*a*comp))) for a in RED)+(0.5,))
		#	background.append((r*x,r*y,r*z)+tuple(50+0.25*x for x in aSphere.colors[i])+(1.0,))

	#Calculate and add "Target Point on Sphere", i.e. the optimal choice of position given the opponents current position
	b = aO.w
	B0 =  b[0]*0.0 + b[1]/1.4 + b[2]/2.0
	B1 =  b[0]/1.4 + b[1]*0.0 - b[2]/2.0
	B2 =  b[0]*0.0 - b[1]/1.4 + b[2]/2.0
	B3 = -b[0]/1.4 + b[1]*0.0 - b[2]/2.0
	v4 = (B2-B1, B3-B2, B0-B3, B1-B0)
	v3 = (v4[1]/1.4-v4[3]/1.4, v4[0]/1.4-v4[2]/1.4, v4[0]/2.0-v4[1]/2.0+v4[2]/2.0-v4[3]/2.0)
	x0 = (aP.u[0]*v3[0]+aP.u[1]*v3[1]+aP.u[2]*v3[2])/m.sqrt(3.0)
	y0 = (aP.v[0]*v3[0]+aP.v[1]*v3[1]+aP.v[2]*v3[2])/m.sqrt(3.0)
	z0 = (aP.w[0]*v3[0]+aP.w[1]*v3[1]+aP.w[2]*v3[2])/m.sqrt(3.0)
	# something's wrong with the radius normalization here, but the angular position looks right
	if z0 >= 0.0:
		foreground.append((x0,y0,z0)+GREEN+(2.0,))
		background.append((-x0,-y0,-z0)+RED+(2.0,))
	else:
		background.append((x0,y0,z0)+GREEN+(2.0,))
		foreground.append((-x0,-y0,-z0)+RED+(2.0,))

	xSafe = (aP.u[0]+aP.u[1]+aP.u[2])/1.73
	ySafe = (aP.v[0]+aP.v[1]+aP.v[2])/1.73
	zSafe = (aP.w[0]+aP.w[1]+aP.w[2])/1.73
###	if zSafe >= 0.0:
###		foreground.append((xSafe,ySafe,zSafe,255,255,255,1.0))
###		background.append((-xSafe,-ySafe,-zSafe,255,255,255,1.0))
###	else:
###		background.append((xSafe,ySafe,zSafe,255,255,255,1.0))
###		foreground.append((-xSafe,-ySafe,-zSafe,255,255,255,1.0))

	g1 = (aO.w[2], aO.w[0], aO.w[1])
	g2 = (-aO.w[1], -aO.w[2], -aO.w[0])
	x1 = aP.u[0]*g1[0]+aP.u[1]*g1[1]+aP.u[2]*g1[2]
	y1 = aP.v[0]*g1[0]+aP.v[1]*g1[1]+aP.v[2]*g1[2]
	z1 = aP.w[0]*g1[0]+aP.w[1]*g1[1]+aP.w[2]*g1[2]
	x2 = aP.u[0]*g2[0]+aP.u[1]*g2[1]+aP.u[2]*g2[2]
	y2 = aP.v[0]*g2[0]+aP.v[1]*g2[1]+aP.v[2]*g2[2]
	z2 = aP.w[0]*g2[0]+aP.w[1]*g2[1]+aP.w[2]*g2[2]
	#test drawing actual optimal goal position
#	n3 = m.sqrt(sum([(a+b)**2 for a,b in zip(g1,g2)]))
#	g3 = tuple((n1+n2)/n3 for n1,n2 in zip(g1,g2))
#	x3 = aP.u[0]*g3[0]+aP.u[1]*g3[1]+aP.u[2]*g3[2]
#	y3 = aP.v[0]*g3[0]+aP.v[1]*g3[1]+aP.v[2]*g3[2]
#	z3 = aP.w[0]*g3[0]+aP.w[1]*g3[1]+aP.w[2]*g3[2]
	#test drawing location of opponent
	g4 = (aO.w[0], aO.w[1], aO.w[2])
	x4 = aP.u[0]*g4[0]+aP.u[1]*g4[1]+aP.u[2]*g4[2]
	y4 = aP.v[0]*g4[0]+aP.v[1]*g4[1]+aP.v[2]*g4[2]
	z4 = aP.w[0]*g4[0]+aP.w[1]*g4[1]+aP.w[2]*g4[2]
#	if z1 >= 0.0:
#		foreground.append((x1,y1,z1)+GREEN)
#		background.append((-x1,-y1,-z1)+RED)
#	else:
#		background.append((x1,y1,z1)+GREEN)
#		foreground.append((-x1,-y1,-z1)+RED)
#	if z2 >= 0.0:
#		foreground.append((x2,y2,z2)+GREEN)
#		background.append((-x2,-y2,-z2)+RED)
#	else:
#		background.append((x2,y2,z2)+GREEN)
#		foreground.append((-x2,-y2,-z2)+RED)
###	if z3 >= 0.0:
###		foreground.append((x3,y3,z3)+GREEN+(1.0,))
###		background.append((-x3,-y3,-z3)+RED+(1.0,))
###	else:
###		background.append((x3,y3,z3)+GREEN+(1.0,))
###		foreground.append((-x3,-y3,-z3)+RED+(1.0,))
###	if z4 >= 0.0:
###		foreground.append((x4,y4,z4)+YELLOW+(2.0,))
###	else:
###		background.append((x4,y4,z4)+YELLOW+(2.0,))

#	for p in range(50):
#		tempG = rotate3Vector((x1,y1,z1), (x3,y3,z3), p*2.0*m.pi/50.)
#		tempZ = aP.w[0]*tempG[0]+aP.w[1]*tempG[1]+aP.w[2]*tempG[2]
###		if tempZ >= 0.0:
###			foreground.append(tempG+GREEN+(0.25,))
###			background.append(tuple(-a for a in tempG)+RED+(0.25,))
###		else:
###			background.append(tempG+GREEN+(0.25,))
###			foreground.append(tuple(-a for a in tempG)+RED+(0.25,))


	for p in background:
		pygame.draw.circle(DISPLAYSURF, p[3:6], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(p[6]*2.5*(p[2]+1.0)**2), 0)
	for p in foreground:
		pygame.draw.circle(DISPLAYSURF, p[3:6], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(p[6]*2.5*(p[2]+1.0)**2), 0)
	
	pygame.draw.circle(DISPLAYSURF, (255.-aP.color[0],255.-aP.color[1],255.-aP.color[2]), (aP.centerX,aP.centerY), 12, 2)


def gameloop(aSphere, aPlayer1, aPlayer2):
	SCORE = 0.0
	scoreColor = (255,255,255)
	while True:
		PCPress1 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 	#w, s, a, d, q, e
		PCPress2 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 	#i, k, j, l, u, o
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
			PCPress1[0] = 1.0
		if press[K_s]:
			PCPress1[1] = 1.0
		if press[K_d]:
			PCPress1[3] = 1.0
		if press[K_a]:
			PCPress1[2] = 1.0
		if press[K_q]:
			PCPress1[4] = 1.0
		if press[K_e]:
			PCPress1[5] = 1.0
		if press[K_i]:
			PCPress2[0] = 1.0
		if press[K_k]:
			PCPress2[1] = 1.0
		if press[K_l]:
			PCPress2[3] = 1.0
		if press[K_j]:
			PCPress2[2] = 1.0
		if press[K_u]:
			PCPress2[4] = 1.0
		if press[K_o]:
			PCPress2[5] = 1.0
		aPlayer1.timeStep(PCPress1, aPlayer2.color)
		aPlayer2.timeStep(PCPress2, aPlayer1.color)
		SCORE -= 1.0*aPlayer1.attack4D(aPlayer2)
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
player2.initMind()
sphere1 = RPSSphere()
gameloop(sphere1,player1,player2)


