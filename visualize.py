# Testing implementation of sphere rotation for RPS battle mechanic
# R Evan McClellan -- 2016-09-06
#

import pygame, sys
from pygame.locals import *
import time
import math as m
from RPSClasses import *

pygame.init()

DISPLAYWIDTH = 1200
DISPLAYHEIGHT = 800

# set up the colors
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
GRAY    = (100, 100, 100)
RED     = (255,   0,   0)
CYAN    = (  0, 255, 255)
GREEN   = (  0, 255,   0)
MAGENTA = (255,   0, 255)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255, 100)

# set up the window
DISPLAYSURF = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), 0, 32)
pygame.display.set_caption("VISUALIZE")

def calcColor(w):
	tempR = min(255, int(255.0 * m.sqrt(max(0.0, w[0])**2.0+max(0.0,-w[1])**2.0+max(0.0,-w[2])**2.0) ))
	tempG = min(255, int(255.0 * m.sqrt(max(0.0,-w[0])**2.0+max(0.0, w[1])**2.0+max(0.0,-w[2])**2.0) ))
	tempB = min(255, int(255.0 * m.sqrt(max(0.0,-w[0])**2.0+max(0.0,-w[1])**2.0+max(0.0, w[2])**2.0) ))
	return (tempR,tempG,tempB)

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

def attack2(a, b):
	#a attacks b
	result = a[0]*(b[2]-b[1]) + a[1]*(b[0]-b[2]) + a[2]*(b[1]-b[0])
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
	#result = A0*(B3-B1) + A1*(B0-B2) + A2*(B1-B3) + A3*(B2-B0)
	result = A0*(B2-B1) + A1*(B3-B2) + A2*(B0-B3) + A3*(B1-B0)
	return result

def drawSphere(aSphere, aP, aO):
	background = []
	foreground = []
	radii = []
	for i,p in enumerate(aSphere.points):
		x = aP.u[0]*p[0]+aP.u[1]*p[1]+aP.u[2]*p[2]
		y = aP.v[0]*p[0]+aP.v[1]*p[1]+aP.v[2]*p[2]
		z = aP.w[0]*p[0]+aP.w[1]*p[1]+aP.w[2]*p[2]
		r = 1.0# - 0.5*abs(p[0]/m.sqrt(3)+p[1]/m.sqrt(3)+p[2]/m.sqrt(3))
		comp = attack4D(p,aO.w)
		if z >= 0.0:
		#	foreground.append((r*x,r*y,r*z)+tuple(50+0.25*x for x in aSphere.colors[i])+(0.5,))
			if comp > 0.0:
				foreground.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(0.5*a*comp))) for a in GREEN)+(0.5,))
			else:
				foreground.append((r*x,r*y,r*z)+tuple(max(0,min(255,int(-0.5*a*comp))) for a in RED)+(0.5,))
		else:
			background.append((r*x,r*y,r*z)+tuple(50+0.25*x for x in aSphere.colors[i])+(0.5,))

	xSafe = (aP.u[0]+aP.u[1]+aP.u[2])/1.73
	ySafe = (aP.v[0]+aP.v[1]+aP.v[2])/1.73
	zSafe = (aP.w[0]+aP.w[1]+aP.w[2])/1.73
	radii.append((xSafe,ySafe,zSafe)+WHITE+(1.0,))
	radii.append((-xSafe,-ySafe,-zSafe)+WHITE+(1.0,))
	radii.append((aP.u[0],aP.v[0],aP.w[0])+RED+(1.0,))
	radii.append((aP.u[1],aP.v[1],aP.w[1])+GREEN+(1.0,))
	radii.append((aP.u[2],aP.v[2],aP.w[2])+BLUE+(1.0,))
	radii.append((-aP.u[0],-aP.v[0],-aP.w[0])+CYAN+(1.0,))
	radii.append((-aP.u[1],-aP.v[1],-aP.w[1])+MAGENTA+(1.0,))
	radii.append((-aP.u[2],-aP.v[2],-aP.w[2])+YELLOW+(1.0,))
	if zSafe >= 0.0:
		foreground.append((xSafe,ySafe,zSafe,255,255,255,1.0))
		background.append((-xSafe,-ySafe,-zSafe,255,255,255,1.0))
	else:
		background.append((xSafe,ySafe,zSafe,255,255,255,1.0))
		foreground.append((-xSafe,-ySafe,-zSafe,255,255,255,1.0))


	#draw red, green, blue, cyan, magenta, yellow axes within the sphere (line from center to surface)
	#draw white axis from safe point to safe point through center of sphere
	#draw rainbow of rays from center out to equator

	for p in range(100):
		tempE = rotate3Vector((1.0/m.sqrt(2.0),-1.0/m.sqrt(2.0),0.0), (0.58,0.58,0.58), p*2.0*m.pi/100.0)
		tempX = aP.u[0]*tempE[0]+aP.u[1]*tempE[1]+aP.u[2]*tempE[2]
		tempY = aP.v[0]*tempE[0]+aP.v[1]*tempE[1]+aP.v[2]*tempE[2]
		tempZ = aP.w[0]*tempE[0]+aP.w[1]*tempE[1]+aP.w[2]*tempE[2]
		comp = attack2(tempE, aO.w)
		if tempZ >= 0.0:
		#	foreground.append((tempX,tempY,tempZ)+calcColor(tempE)+(1.0,))
			if comp > 0.0:
				foreground.append((tempX,tempY,tempZ)+tuple(max(0,min(255,int(0.5*a*comp))) for a in GREEN)+(1.0,))
			else:
				foreground.append((tempX,tempY,tempZ)+tuple(max(0,min(255,int(-0.5*a*comp))) for a in RED)+(1.0,))
		else:
		#	background.append((tempX,tempY,tempZ)+calcColor(tempE)+(1.0,))
			if comp > 0.0:
				background.append((tempX,tempY,tempZ)+tuple(max(0,min(255,int(0.5*a*comp))) for a in GREEN)+(1.0,))
			else:
				background.append((tempX,tempY,tempZ)+tuple(max(0,min(255,int(-0.5*a*comp))) for a in RED)+(1.0,))

	g1 = (aO.w[2], aO.w[0], aO.w[1])
	g2 = (-aO.w[1], -aO.w[2], -aO.w[0])
	x1 = aP.u[0]*g1[0]+aP.u[1]*g1[1]+aP.u[2]*g1[2]
	y1 = aP.v[0]*g1[0]+aP.v[1]*g1[1]+aP.v[2]*g1[2]
	z1 = aP.w[0]*g1[0]+aP.w[1]*g1[1]+aP.w[2]*g1[2]
	x2 = aP.u[0]*g2[0]+aP.u[1]*g2[1]+aP.u[2]*g2[2]
	y2 = aP.v[0]*g2[0]+aP.v[1]*g2[1]+aP.v[2]*g2[2]
	z2 = aP.w[0]*g2[0]+aP.w[1]*g2[1]+aP.w[2]*g2[2]
	#test drawing actual optimal goal position
	n3 = m.sqrt(sum([(a+b)**2 for a,b in zip(g1,g2)]))
	g3 = tuple((n1+n2)/n3 for n1,n2 in zip(g1,g2))
	x3 = aP.u[0]*g3[0]+aP.u[1]*g3[1]+aP.u[2]*g3[2]
	y3 = aP.v[0]*g3[0]+aP.v[1]*g3[1]+aP.v[2]*g3[2]
	z3 = aP.w[0]*g3[0]+aP.w[1]*g3[1]+aP.w[2]*g3[2]
	#test drawing location of opponent
	g4 = (aO.w[0], aO.w[1], aO.w[2])
	x4 = aP.u[0]*g4[0]+aP.u[1]*g4[1]+aP.u[2]*g4[2]
	y4 = aP.v[0]*g4[0]+aP.v[1]*g4[1]+aP.v[2]*g4[2]
	z4 = aP.w[0]*g4[0]+aP.w[1]*g4[1]+aP.w[2]*g4[2]
#	if z1 >= 0.0:
#		foreground.append((x1,y1,z1)+GREEN+(1.0,))
#		background.append((-x1,-y1,-z1)+RED+(1.0,))
#	else:
#		background.append((x1,y1,z1)+GREEN+(1.0,))
#		foreground.append((-x1,-y1,-z1)+RED+(1.0,))
#	if z2 >= 0.0:
#		foreground.append((x2,y2,z2)+GREEN+(1.0,))
#		background.append((-x2,-y2,-z2)+RED+(1.0,))
#	else:
#		background.append((x2,y2,z2)+GREEN+(1.0,))
#		foreground.append((-x2,-y2,-z2)+RED+(1.0,))
	if z3 >= 0.0:
		foreground.append((x3,y3,z3)+GREEN+(2.0,))
		background.append((-x3,-y3,-z3)+RED+(2.0,))
	else:
		background.append((x3,y3,z3)+GREEN+(2.0,))
		foreground.append((-x3,-y3,-z3)+RED+(2.0,))
	if z4 >= 0.0:
		foreground.append((x4,y4,z4)+YELLOW+(2.0,))
	else:
		background.append((x4,y4,z4)+YELLOW+(2.0,))

	for p in range(50):
		tempG = rotate3Vector((x1,y1,z1), (x3,y3,z3), p*2.0*m.pi/50.)
		tempZ = aP.w[0]*tempG[0]+aP.w[1]*tempG[1]+aP.w[2]*tempG[2]
		if tempZ >= 0.0:
			foreground.append(tuple(g for g in tempG)+GREEN+(0.25,))
			background.append(tuple(-a for a in tempG)+RED+(0.25,))
		else:
			background.append(tuple(g for g in tempG)+GREEN+(0.25,))
			foreground.append(tuple(-a for a in tempG)+RED+(0.25,))


	for p in background:
		pygame.draw.circle(DISPLAYSURF, p[3:6], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(p[6]*2.5*(p[2]+1.0)**2), 0)
	for r in radii:
		pygame.draw.line(DISPLAYSURF, r[3:6], (aP.centerX, aP.centerY), (int(200.0*r[0]+aP.centerX),int(200.0*r[1]+aP.centerY)), int(r[6]))
	for p in foreground:
		pygame.draw.circle(DISPLAYSURF, p[3:6], (int(200.0*p[0]+aP.centerX),int(200.0*p[1]+aP.centerY)), int(p[6]*2.5*(p[2]+1.0)**2), 0)
	
	pygame.draw.circle(DISPLAYSURF, (255.-aP.color[0],255.-aP.color[1],255.-aP.color[2]), (aP.centerX,aP.centerY), 12, 2)


def gameloop(aSphere, aPlayer1, aPlayer2):
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
			aPlayer1.uVelocity += 0.01
		if press[K_s]:
			aPlayer1.uVelocity += -0.01
		if press[K_d]:
			aPlayer1.vVelocity += 0.01
		if press[K_a]:
			aPlayer1.vVelocity += -0.01
		if press[K_q]:
			aPlayer1.wVelocity += 0.01
		if press[K_e]:
			aPlayer1.wVelocity += -0.01
		if press[K_f]:
			aPlayer1.uVelocity += -0.1*aPlayer1.uVelocity
			aPlayer1.vVelocity += -0.1*aPlayer1.vVelocity
			aPlayer1.wVelocity += -0.1*aPlayer1.wVelocity
		if press[K_SPACE]:
			print aPlayer1.w
		if press[K_i]:
			aPlayer2.uVelocity += 0.01
		if press[K_k]:
			aPlayer2.uVelocity += -0.01
		if press[K_l]:
			aPlayer2.vVelocity += 0.01
		if press[K_j]:
			aPlayer2.vVelocity += -0.01
		if press[K_u]:
			aPlayer2.wVelocity += 0.01
		if press[K_o]:
			aPlayer2.wVelocity += -0.01
		if press[K_h]:
			aPlayer2.uVelocity += -0.1*aPlayer2.uVelocity
			aPlayer2.vVelocity += -0.1*aPlayer2.vVelocity
			aPlayer2.wVelocity += -0.1*aPlayer2.wVelocity
		aPlayer1.uVelocity += -0.01*aPlayer1.uVelocity
		aPlayer1.vVelocity += -0.01*aPlayer1.vVelocity
		aPlayer1.wVelocity += -0.01*aPlayer1.wVelocity
		aPlayer2.uVelocity += -0.01*aPlayer2.uVelocity
		aPlayer2.vVelocity += -0.01*aPlayer2.vVelocity
		aPlayer2.wVelocity += -0.01*aPlayer2.wVelocity
		aPlayer1.timestep()
		aPlayer2.timestep()
		aPlayer1.calcColor()
		aPlayer2.calcColor()
		DISPLAYSURF.fill(BLACK)
		drawSphere(aSphere, aPlayer1, aPlayer2)
		drawSphere(aSphere, aPlayer2, aPlayer1)
		pygame.display.update()
		time.sleep(0.02)

player1 = RPSPlayerInertia(300,400,1.0)
player2 = RPSPlayerInertia(900,400,-1.0)
#player2 = RPSNeuralInertia(900,400,-1.0)
sphere1 = RPSSphere()
gameloop(sphere1,player1,player2)


