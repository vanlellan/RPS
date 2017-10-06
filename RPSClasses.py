#Classes for RPS games: Quaternion, RPSPlayer, RPSSphere
import math as m
import numpy as np
import random as r

class Quaternion():
	#notes:
	# x  1  i  j  k
	# 1  1  i  j  k
	# i  i -1  k -j
	# j  j -k -1  i
	# k  k  j -i -1

	def __init__(self, q0, q1, q2, q3):
		self.comp = [q0,q1,q2,q3]

	def conjugate(self):
		self.comp[1] = -self.comp[1]
		self.comp[2] = -self.comp[2]
		self.comp[3] = -self.comp[3]

	def multR(self, aOther):
		new = [0.0,0.0,0.0,0.0]
		new[0] = self.comp[0]*aOther.comp[0] - self.comp[1]*aOther.comp[1] - self.comp[2]*aOther.comp[2] - self.comp[3]*aOther.comp[3]
		new[1] = self.comp[0]*aOther.comp[1] + self.comp[1]*aOther.comp[0] + self.comp[2]*aOther.comp[3] - self.comp[3]*aOther.comp[2]
		new[2] = self.comp[0]*aOther.comp[2] - self.comp[1]*aOther.comp[3] + self.comp[2]*aOther.comp[0] + self.comp[3]*aOther.comp[1]
		new[3] = self.comp[0]*aOther.comp[3] + self.comp[1]*aOther.comp[2] - self.comp[2]*aOther.comp[1] + self.comp[3]*aOther.comp[0]
		self.comp = new

	def multL(self, aOther):
		new = [0.0,0.0,0.0,0.0]
		new[0] = aOther.comp[0]*self.comp[0] - aOther.comp[1]*self.comp[1] - aOther.comp[2]*self.comp[2] - aOther.comp[3]*self.comp[3]
		new[1] = aOther.comp[0]*self.comp[1] + aOther.comp[1]*self.comp[0] + aOther.comp[2]*self.comp[3] - aOther.comp[3]*self.comp[2]
		new[2] = aOther.comp[0]*self.comp[2] - aOther.comp[1]*self.comp[3] + aOther.comp[2]*self.comp[0] + aOther.comp[3]*self.comp[1]
		new[3] = aOther.comp[0]*self.comp[3] + aOther.comp[1]*self.comp[2] - aOther.comp[2]*self.comp[1] + aOther.comp[3]*self.comp[0]
		self.comp = new


class RPSDummy():
	#notes
	def __init__(self):
		self.w = [0.0,0.0,1.0]
		self.colors = (255,255,255)

	def seed(self):
		r.seed()

	def randomize(self):
		theta = r.uniform(0.0,m.pi)
		phi = r.uniform(0.0,2.0*m.pi)
		self.w = [m.cos(theta)*m.sin(phi), m.sin(theta)*m.sin(phi), m.cos(phi)]

		tempR = int(255.0 * m.sqrt(max(0.0, self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempG = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0, self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempB = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0, self.w[2])**2.0) )
		self.colors = (tempR,tempG,tempB)

	# More complicated than needed here, but potentially useful for other applications
	#	wXz = [(1.0/m.sqrt(w[0]**2.0+w[1]**2.0))*w[1],-(1.0/m.sqrt(w[0]**2.0+w[1]**2.0))*w[0],0.0]
	#	wQ = Quaternion(0.0,self.w[0],self.w[1],self.w[2])
	#	A = m.cos(m.pi/4.0)
	#	B = m.sin(m.pi/4.0)
	#	q = Quaternion(A,B*wXz[0],B*wXz[1],B*wXz[2])

class RPSPlayer():
	#notes:
	def __init__(self,aX,aY,sign):
		self.centerX = aX
		self.centerY = aY
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.speed = 0.05
		self.calcColor()
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

	def reset(self,sign):
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

	def calcColor(self):
		tempR = int(255.0 * m.sqrt(max(0.0, self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempG = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0, self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempB = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0, self.w[2])**2.0) )
		self.color = (tempR,tempG,tempB)

	def rotate(self,axis,spin,theta):
		a = m.cos(theta/2.0)
		b = m.sin(theta/2.0)
		q = Quaternion(a, spin*axis[0]*b, spin*axis[1]*b, spin*axis[2]*b)
		uQ = Quaternion(0.0, self.u[0], self.u[1], self.u[2])
		uQ.multL(q)
		q.conjugate()
		uQ.multR(q)
		self.u[0] = uQ.comp[1]
		self.u[1] = uQ.comp[2]
		self.u[2] = uQ.comp[3]
		vQ = Quaternion(0.0, self.v[0], self.v[1], self.v[2])
		q.conjugate()
		vQ.multL(q)
		q.conjugate()
		vQ.multR(q)
		self.v[0] = vQ.comp[1]
		self.v[1] = vQ.comp[2]
		self.v[2] = vQ.comp[3]
		wQ = Quaternion(0.0, self.w[0], self.w[1], self.w[2])
		q.conjugate()
		wQ.multL(q)
		q.conjugate()
		wQ.multR(q)
		self.w[0] = wQ.comp[1]
		self.w[1] = wQ.comp[2]
		self.w[2] = wQ.comp[3]

class RPSSphere():
	#notes:
	def __init__(self):
		thetaList = [float(x)*m.pi/24.0 for x in range(25)]
		rPerp = [m.sin(x) for x in thetaList]
		phiListList = []
		for rp in rPerp:
			num = 1+int(60.0*rp)
			phiListList.append([float(x)*2.0*m.pi/float(num) for x in range(num)])
		self.points = []
		self.colors = []
		for i,th in enumerate(thetaList):
			for ph in phiListList[i]:
				x = m.cos(ph)*m.sin(th)
				y = m.sin(ph)*m.sin(th)
				z = m.cos(th)
				ang = m.atan(m.sqrt(2.0))
				q45xy = Quaternion(m.cos(ang/2.0), -m.sin(ang/2.0)/m.sqrt(2.0), m.sin(ang/2.0)/m.sqrt(2.0), 0.0)
				qP = Quaternion(0.0, x, y, z)
				qP.multL(q45xy)
				q45xy.conjugate()
				qP.multR(q45xy)
				self.points.append((qP.comp[1], qP.comp[2], qP.comp[3]))
		for p in self.points:	# non-pure colors are not maximally bright, brighten all colors?
			tempR = int(255.0 * m.sqrt(max(0.0, p[0])**2.0+max(0.0,-p[1])**2.0+max(0.0,-p[2])**2.0) )
			tempG = int(255.0 * m.sqrt(max(0.0,-p[0])**2.0+max(0.0, p[1])**2.0+max(0.0,-p[2])**2.0) )
			tempB = int(255.0 * m.sqrt(max(0.0,-p[0])**2.0+max(0.0,-p[1])**2.0+max(0.0, p[2])**2.0) )
			ratio = 255/max(tempR, tempG, tempB) #simple attempt at brightening
			self.colors.append((tempR*ratio,tempG*ratio,tempB*ratio))

class RPSPlayerInertia():
	#notes:
	def __init__(self,aX,aY,sign):
		self.points = 0
		self.centerX = aX
		self.centerY = aY
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.uVelocity = 0.0
		self.vVelocity = 0.0
		self.wVelocity = 0.0
		self.calcColor()
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

	def reset(self,sign):
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.uVelocity = 0.0
		self.vVelocity = 0.0
		self.wVelocity = 0.0
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

	def calcColor(self):
		tempR = int(255.0 * m.sqrt(max(0.0, self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempG = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0, self.w[1])**2.0+max(0.0,-self.w[2])**2.0) )
		tempB = int(255.0 * m.sqrt(max(0.0,-self.w[0])**2.0+max(0.0,-self.w[1])**2.0+max(0.0, self.w[2])**2.0) )
		self.color = (tempR,tempG,tempB)

	def timestep(self):
		magSpeed = m.sqrt(self.uVelocity**2.0 + self.vVelocity**2.0 + self.wVelocity**2.0)
		uLimited = 0.05*self.uVelocity/(0.04+magSpeed)
		vLimited = 0.05*self.vVelocity/(0.04+magSpeed)
		wLimited = 0.05*self.wVelocity/(0.04+magSpeed)
		self.rotate(self.u,1.0,uLimited)
		self.rotate(self.v,1.0,vLimited)
		self.rotate(self.w,1.0,wLimited)

	def rotate(self,axis,spin,theta):
		a = m.cos(theta/2.0)
		b = m.sin(theta/2.0)
		q = Quaternion(a, spin*axis[0]*b, spin*axis[1]*b, spin*axis[2]*b)
		uQ = Quaternion(0.0, self.u[0], self.u[1], self.u[2])
		uQ.multL(q)
		q.conjugate()
		uQ.multR(q)
		self.u[0] = uQ.comp[1]
		self.u[1] = uQ.comp[2]
		self.u[2] = uQ.comp[3]
		vQ = Quaternion(0.0, self.v[0], self.v[1], self.v[2])
		q.conjugate()
		vQ.multL(q)
		q.conjugate()
		vQ.multR(q)
		self.v[0] = vQ.comp[1]
		self.v[1] = vQ.comp[2]
		self.v[2] = vQ.comp[3]
		wQ = Quaternion(0.0, self.w[0], self.w[1], self.w[2])
		q.conjugate()
		wQ.multL(q)
		q.conjugate()
		wQ.multR(q)
		self.w[0] = wQ.comp[1]
		self.w[1] = wQ.comp[2]
		self.w[2] = wQ.comp[3]

class RPSNeuralInertia(RPSPlayerInertia):
	def __init__(self,aX,aY,sign):
		RPSPlayerInertia.__init__(self,aX,aY,sign)
		self.M1 = np.random.rand(16,6) - 0.5
		self.B1 = np.random.rand(16,1) - 0.5*6
		self.M2 = np.random.rand(7,16) - 0.5
		self.B2 = np.random.rand(7,1) - 0.5*16
		self.B3 = np.random.rand(7,1) - 0.5
		self.press = [0,0,0,0,0,0,0]

	def timestep(self):
		self.uVelocity += 0.01*(self.press[0] - self.press[1])
		self.vVelocity += 0.01*(self.press[2] - self.press[3])
		self.wVelocity += 0.01*(self.press[4] - self.press[5])
		magSpeed = m.sqrt(self.uVelocity**2.0 + self.vVelocity**2.0 + self.wVelocity**2.0)
		uLimited = 0.05*self.uVelocity/(0.04+magSpeed)
		vLimited = 0.05*self.vVelocity/(0.04+magSpeed)
		wLimited = 0.05*self.wVelocity/(0.04+magSpeed)
		self.rotate(self.u,1.0,uLimited)
		self.rotate(self.v,1.0,vLimited)
		self.rotate(self.w,1.0,wLimited)

	def brain(self, opponentColor):
		# nrow x ncol
		# I  is 6x1
		# O  is 7x1
		# H  is 16x1
		# M1 is 16x6
		# B1 is 16x1
		# M2 is 7x16
		# B2 is 7x1
		# B3 is 7x1
		I = np.array([float(x)/255. for x in self.color+opponentColor]).reshape(6,1)
		H = 1.0/(1.0+np.exp(-(np.dot(self.M1,I)+self.B1)))
		O = 1.0/(1.0+np.exp(-(np.dot(self.M2,H)+self.B2)))
		O = 0.5 * (np.sign(O+self.B3) + 1.0)
		self.press = [x for x in O.reshape(7)]
		print self.u
		print self.v
		print self.w




