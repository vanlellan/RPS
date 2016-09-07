#Classes for RPS games: Quaternion, RPSPlayer, RPSSphere
import numpy as np
import math as m


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



class RPSPlayer():
	#notes:
	def __init__(self):
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,1.0,0.0]
		self.w = [0.0,0.0,1.0]
		self.scalarSpeed = m.cos(0.1/2.0)
		self.vectorSpeed = m.sin(0.1/2.0)

	def rotate(self,axis,spin):
		q = Quaternion(self.scalarSpeed, spin*axis[0]*self.vectorSpeed, spin*axis[1]*self.vectorSpeed, spin*axis[2]*self.vectorSpeed)
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
		thetaList = np.arange(0.0,np.pi,0.05)
		phiList = np.arange(0.0,2.0*np.pi,0.05)
		self.points = []
		self.colors = []
		for ph in phiList:
			for th in thetaList:
				self.points.append((m.cos(th)*m.sin(ph), m.sin(th)*m.sin(ph), m.cos(ph)))
		for p in self.points:
			tempR = int(255.0 * m.sqrt(max(0.0, p[0])**2.0+max(0.0,-p[1])**2.0+max(0.0,-p[2])**2.0) )
			tempG = int(255.0 * m.sqrt(max(0.0,-p[0])**2.0+max(0.0, p[1])**2.0+max(0.0,-p[2])**2.0) )
			tempB = int(255.0 * m.sqrt(max(0.0,-p[0])**2.0+max(0.0,-p[1])**2.0+max(0.0, p[2])**2.0) )
			self.colors.append((tempR,tempG,tempB))

