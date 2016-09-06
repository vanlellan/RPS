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
from quaternionClass import quaternion

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
pygame.display.set_caption('Thing')

#HARD CODE AMOUNT OF ROTATION PER KEYPRESS (0.1 radians)
costhh = m.cos(0.1/2.0)
sinthh = m.sin(0.1/2.0)

u = [1.0,0.0,0.0]
v = [0.0,1.0,0.0]
w = [0.0,0.0,1.0]


thetaList = np.arange(0.0,np.pi,0.1)
phiList = np.arange(0.0,2.0*np.pi,0.2)
points = []
for ph in phiList:
	for th in thetaList:
		points.append((m.cos(th)*m.sin(ph), m.sin(th)*m.sin(ph), m.cos(ph)))


def drawCircle():
	DISPLAYSURF.fill(BLACK)
	for p in points:
		if (w[0]*p[0]+w[1]*p[1]+w[2]*p[2]) >= 0.0:
			if (p[2]) >= 0.0:
				pygame.draw.circle(DISPLAYSURF, RED, (int(200.0*(u[0]*p[0]+u[1]*p[1]+u[2]*p[2]))+600,int(200.0*(v[0]*p[0]+v[1]*p[1]+v[2]*p[2]))+400), 5, 0)
			else:
				pygame.draw.circle(DISPLAYSURF, GRAY, (int(200.0*(u[0]*p[0]+u[1]*p[1]+u[2]*p[2]))+600,int(200.0*(v[0]*p[0]+v[1]*p[1]+v[2]*p[2]))+400), 5, 0)

def rotateSphere(a,sign):
	global u
	global v
	global w
	q = quaternion(costhh, sign*a[0]*sinthh, sign*a[1]*sinthh, sign*a[2]*sinthh)
	uQ = quaternion(0.0, u[0], u[1], u[2])
	uQ.multL(q)
	q.conjugate()
	uQ.multR(q)
	u[0] = uQ.comp[1]
	u[1] = uQ.comp[2]
	u[2] = uQ.comp[3]
	vQ = quaternion(0.0, v[0], v[1], v[2])
	q.conjugate()
	vQ.multL(q)
	q.conjugate()
	vQ.multR(q)
	v[0] = vQ.comp[1]
	v[1] = vQ.comp[2]
	v[2] = vQ.comp[3]
	wQ = quaternion(0.0, w[0], w[1], w[2])
	q.conjugate()
	wQ.multL(q)
	q.conjugate()
	wQ.multR(q)
	w[0] = wQ.comp[1]
	w[1] = wQ.comp[2]
	w[2] = wQ.comp[3]

def gameloop():
	global u
	global v
	global w
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
				elif event.key == K_RETURN:
					stepToggle = not stepToggle
				elif event.key == K_i:
					#positive rotation around u-axis
					rotateSphere(u,1.0)
				elif event.key == K_k:
					rotateSphere(u,-1.0)
				elif event.key == K_l:
					rotateSphere(v,1.0)
				elif event.key == K_j:
					rotateSphere(v,-1.0)
				elif event.key == K_u:
					rotateSphere(w,1.0)
				elif event.key == K_o:
					rotateSphere(w,-1.0)
		drawCircle()
		pygame.display.update()
		time.sleep(0.02)


gameloop()


