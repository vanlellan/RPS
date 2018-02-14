#Classes for RPS games: Quaternion, RPSPlayer, RPSSphere
import math as m
import numpy as np
import random as r
import pickle

#I really need to go back and rewrite the basic player class. The inertia class would inherit from it. Turning on the Neural Control would be a switch.


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

class RPSPlayer():
	#notes:
	def __init__(self,aX,aY,sign):
		self.points = 0
		self.centerX = aX
		self.centerY = aY
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.speed = 0.05
		self.AIFlag = False
		self.calcColor()
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

	def initMind(self):
		self.AIFlag = True
		self.NNdim = [3,16,7]
		self.M1 = 2.0*np.random.rand(self.NNdim[1],self.NNdim[0]) - 1.0
		self.B1 = 2.0*self.NNdim[0]*np.random.rand(self.NNdim[1]) - 1.0*self.NNdim[0]
		self.M2 = 2.0*np.random.rand(self.NNdim[2],self.NNdim[1]) - 1.0
		self.B2 = 2.0*self.NNdim[1]*np.random.rand(self.NNdim[2]) - 1.0*self.NNdim[1]
		self.histLen = 1000
		self.myHist = np.zeros(self.histLen, dtype=(int,12))	#combine these into one length=6 tuple
		self.stepCount = 0

	def think(self, OPw):
		OpX = self.u[0]*OPw[0]+self.u[1]*OPw[1]+self.u[2]*OPw[2]
		OpY = self.v[0]*OPw[0]+self.v[1]*OPw[1]+self.v[2]*OPw[2]
		OpZ = self.w[0]*OPw[0]+self.w[1]*OPw[1]+self.w[2]*OPw[2]
		self.myHist[self.stepCount] = self.u + self.v + self.w + [a for a in OPw]
		self.stepCount += 1
		if self.stepCount == self.histLen:
			self.stepCount = 0
			with open("Hist.pickle","wb") as pickleFile:
				pickle.dump(self.myHist, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)
			print "History Picked and Saved!"
		# nrow x ncol
		# I  is 3x1	3	--input layer of nodes
		# O  is 7x1	7	--output layer of nodes
		# H  is 16x1	16	--hidden layer of nodes
		# M1 is 16x3	48	--weight matrix between I and H
		# B1 is 16x1	16	--bias applied when filling H
		# M2 is 7x16	112	--weight matrix between H and O
		# B2 is 7x1	7	--bias applied when filling O
		# Total number of fit parameters = 209
		#I = np.array([float(x)/255. for x in self.u+self.v+self.w+list(opponentColor)]).reshape(self.NNdim[0],1)
		I = np.array([OpX, OpY, OpZ])
		H = 1.0/(1.0+np.exp(-np.add(np.dot(self.M1,I),self.B1)))
		O = 1.0/(1.0+np.exp(-np.add(np.dot(self.M2,H),self.B2)))
		return O.reshape(self.NNdim[2])

	def calcTarget4D(self, aOw):
		#Calculate "Target Point on Sphere", i.e. the optimal choice of position given the opponents current position
		b = aOw
		B0 =  b[0]*0.0 + b[1]/1.4 + b[2]/2.0
		B1 =  b[0]/1.4 + b[1]*0.0 - b[2]/2.0
		B2 =  b[0]*0.0 - b[1]/1.4 + b[2]/2.0
		B3 = -b[0]/1.4 + b[1]*0.0 - b[2]/2.0
		v4 = (B2-B1, B3-B2, B0-B3, B1-B0)
		v3 = (v4[1]/1.4-v4[3]/1.4, v4[0]/1.4-v4[2]/1.4, v4[0]/2.0-v4[1]/2.0+v4[2]/2.0-v4[3]/2.0)
		magv3 = m.sqrt(v3[0]**2 + v3[1]**2 + v3[2]**2)	#I'm not sure why the normalization isn't already correct here...
		return tuple(i/magv3 for i in v3)

	def attack4D(self, aP2):
		#self attacks aP2 in FOUR DIMENSIONS (use 1.4 for sqrt(2))
		a = self.w
		b = aP2.w
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

	def timeStep(self, PCPress, OpCol):
		if self.AIFlag:
			factor = self.think(self.calcTarget4D(OpCol))
		else:
			factor = PCPress
		self.rotate(self.u, 1.0, self.speed*factor[0])
		self.rotate(self.u,-1.0, self.speed*factor[1])
		self.rotate(self.v, 1.0, self.speed*factor[3])
		self.rotate(self.v,-1.0, self.speed*factor[2])
		self.rotate(self.w, 1.0, self.speed*factor[4])
		self.rotate(self.w,-1.0, self.speed*factor[5])
		self.calcColor()

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

class RPSPlayerInertia(RPSPlayer):
	#notes:
	def __init__(self,aX,aY,sign):
		RPSPlayer.__init__(self,aX,aY,sign)
		self.uVelocity = 0.0
		self.vVelocity = 0.0
		self.wVelocity = 0.0
		
	def timestep(self):
		magSpeed = m.sqrt(self.uVelocity**2.0 + self.vVelocity**2.0 + self.wVelocity**2.0)
		uLimited = 0.05*self.uVelocity/(0.04+magSpeed)
		vLimited = 0.05*self.vVelocity/(0.04+magSpeed)
		wLimited = 0.05*self.wVelocity/(0.04+magSpeed)
		self.rotate(self.u,1.0,uLimited)
		self.rotate(self.v,1.0,vLimited)
		self.rotate(self.w,1.0,wLimited)

	def reset(self,sign):
		sign = float(sign)/abs(sign)
		self.u = [1.0,0.0,0.0]
		self.v = [0.0,sign,0.0]
		self.w = [0.0,0.0,sign]
		self.uVelocity = 0.0
		self.vVelocity = 0.0
		self.wVelocity = 0.0
		self.rotate((-1.0/m.sqrt(2.0),1.0/m.sqrt(2.0),0.0), 1.0, m.atan(m.sqrt(2.0)))

class RPSNeuralInertia(RPSPlayerInertia):
	def __init__(self,aX,aY,sign):
		RPSPlayerInertia.__init__(self,aX,aY,sign)
		self.NNdim = [12,16,7]
		self.M1 = 2.0*np.random.rand(self.NNdim[1],self.NNdim[0]) - 1.0
		self.B1 = 2.0*self.NNdim[0]*np.random.rand(self.NNdim[1],1) - 1.0*self.NNdim[0]
		self.M2 = 2.0*np.random.rand(self.NNdim[2],self.NNdim[1]) - 1.0
		self.B2 = 2.0*self.NNdim[1]*np.random.rand(self.NNdim[2],1) - 1.0*self.NNdim[1]
		self.B3 = 2.0*np.random.rand(self.NNdim[2],1) - 1.0
		self.press = np.zeros(self.NNdim[2])
		self.histLen = 1000
		self.myHist = np.zeros(self.histLen, dtype=(int,3))	#combine these into one length=6 tuple
		self.opHist = np.zeros(self.histLen, dtype=(int,3))	#combine these into one length=6 tuple
		self.stepCount = 0

	def timestep(self):
		self.stepCount += 1
		if self.stepCount == self.histLen:
			self.stepCount = 0
			#pickle myHist and opHist and save as a file
			with open("aiHist.pickle","wb") as pickleFile:
				pickle.dump(self.myHist, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)
			with open("pcHist.pickle","wb") as pickleFile:
				pickle.dump(self.opHist, pickleFile, protocol=pickle.HIGHEST_PROTOCOL)

# temporarily saved for ease: how to read the pickeled data 
#	with open("tags.pickle","rb") as pickleFile:
#		tagDict = pickle.load(pickleFile)

			print "Game Histories Saved and Reset."
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
		#self.myHist = np.concatenate((self.myHist[1:], [self.color]), axis=0)
		#self.opHist = np.concatenate((self.opHist[1:], [opponentColor]), axis=0)
		self.myHist[self.stepCount] = self.color
		self.myHist[self.stepCount] = opponentColor
		# nrow x ncol
		# I  is 12x1	--input layer of nodes
		# O  is 7x1	--output layer of nodes
		# H  is 16x1	--hidden layer of nodes
		# M1 is 16x12	--weight matrix between I and H
		# B1 is 16x1	--bias applied when filling H
		# M2 is 7x16	--weight matrix between H and O
		# B2 is 7x1	--bias applied when filling O
		# B3 is 7x1	--bias applied when thresholding O
		# Total number of fit parameters = 334
			#need to input both opponent position and self position and orientation
			#alternatively, calculate opponent relative position and use that as NN input
		I = np.array([float(x)/255. for x in self.u+self.v+self.w+list(opponentColor)]).reshape(self.NNdim[0],1)
	#	print I.reshape(12)
		H = 1.0/(1.0+np.exp(-(np.dot(self.M1,I)+self.B1)))
	#	print H.reshape(16)
		O = 1.0/(1.0+np.exp(-(np.dot(self.M2,H)+self.B2)))
	#	print "O     = ", O.reshape(7)
		O = 0.5 * (np.sign(O+self.B3) + 1.0)
		self.press = O.reshape(self.NNdim[2])
	#	print "press = ", self.press




