import ac
import acsys
import math
from UltimateSpotter_third_party.sound_player import euclid

carLength = 4.3
carWidth = 1.8

class Opponent (object):
	"""Another driver on track."""
	idd = 0
	name = "name"
	model = "model"
	currentWorldPos = None
	currentVelVec = None
	currentTyre = None
	currentSpeed = 0.0
	splineposition = 0.0
	laps = -1
	playerDist = 0.0
	relativePos = 0.0

	shouldBeCalled = False

	def __init__ (self,idd,name,model):
		self.name = name
		self.idd = idd
		self.model = model
		ac.log("SPOTTER: OPPONENT INIT {}: {} driving {}"(self.idd,self.name,self.model))

	def checkForNewDriver(self):
		acname = ac.getDriverName(self.idd)
		if acname == self.name: return False
		self.name = acname
		return True

	def calcPlayer(self):
		speed = ac.getCarState(self.idd,acsys.CS.SpeedKMH)
		if speed < 1:
			self.currentSpeed = 0.0
		else: self.currentSpeed = speed
		x, y, z = ac.getCarState(self.idd,acsys.CS.WorldPosition)
		self.currentWorldPos = euclid.Point2(x, z)
		f, u, l = ac.getCarState(self.idd,acsys.CS.Velocity)
		self.currentVelVec = euclid.Vector2(f,1).normalize()
		self.laps = ac.getCarState(self.idd,acsys.CS.NormalizedSplinePosition)
		self.relativePos = euclid.Point2(0,0)
		self.playerDist = 0

	def calc(self,player):
		if self == player:
			return
		if self.currentSpeed < 1:
			self.currentSpeed = 0.0
			shouldBeCalled = False
		else:
			shouldBeCalled = True
			x, y, z = ac.getCarState(self.idd, acsys.CS.WorldPosition)
			self.currentWorldPos = euclid.Point2(x,z)
			f, u, l = ac.getCarState(self.idd, acsys.CS.Velocity)
			self.currentVelVec = euclid.Vector2(f,l).normalize()
			self.laps = ac.getCarState()
			self.splineposition = ac.getCarState(self.idd,acsys.CS.NormalizedSplinePosition)
			self.relativePos = euclid.Point2(x-player.currentWorldPos.x, z - player.currentWorldPos.y)
			self.playerDist = player.currentWorldPos.distance(euclid.Point2(x,z))

	def calcDrawingInformation (self, playerVectorReversed):
		if self.id != 0:
			angle = math.atan2(-1,0)-math.atan(playerVectorReversed.y,playerVectorReversed.x)
			angleD = angle * 360 / (2*math.pi)
			angleR = angleD * math.pi/180
			cosTheta = math.cos(angleR)
			sinTheta = math.sin(angleR)
			x = cosTheta * self.relativePos.x - sinTheta * self.relativePos.y
			y = sinTheta * self.relativePos.x + cosTheta * self.relativePos.y

			#self.centerPosition = euclid.Point2(x,y);