# UltimateSpotter v0.1
# Created by Davinium
#
# Base code from Stereo's Spotter App
#
# Some code from AE86SpeedChime and RpmBeeper by Klayking and TKu, respectively
#
# Uses Rombik's SimInfo
# 
#
# Based on:
#  http://www.assettocorsa.net/forum/index.php?threads/audible-gear-shift-beep.14237/
#  http://www.assettocorsa.net/forum/index.php?threads/app-request.7234/#post-103371
#  http://www.assettocorsa.net/forum/index.php?threads/ae86-speed-chime-app.41318/
#
#
# Installation:
#  - Extract to your Assetto Corsa/apps/python directory
#  - Activate the app ingame
#

import ac, acsys
import sys
import math
import configparser , platform , os , os.path , traceback
import time
import random

if platform.architecture()[0] == "64bit":
	libdir = 'UltimateSpotter_dll_x64'
else:
	libdir = 'UltimateSpotter_dll_x86'

sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."


from UltimateSpotter_third_party.sim_info import SimInfo
from UltimateSpotter_third_party.sound_player import SoundPlayer

sim_info = SimInfo()


# app window initialization
#NAME = "UltimateSpotter Settings"
#WIDTH = 1300
#HEIGHT = 600
#app = ac.newApp(NAME)
#sound_player = SoundPlayer(AUDIO_UP)

audio = 0
audioList = 0


app = 0

audioSpinner = 0
audioList = 0
audioLabel = 0

audioVol = 0
audioVolSpinner = 0

enableCheck = 0 # is this thing turned on?
replayEnableCheck = 0

##
audio = "JJPack"
USEnabled = True
USReplayEnabled = True

sound = SoundPlayer(os.path.join(os.path.dirname(__file__), "audio//JJPack//n23.wav"))


#READING AUDIO INI
config = configparser.ConfigParser()


lapReset = False
minReset = False
secReset = False


def acMain(ac_version):
	global mainLabel, audioSpinner, audioLabel, audioList, audioVolSpinner, enableCheck, replayEnableCheck, app
	app = ac.newApp ("Ultimate Spotter Settings")
	ac.log ("SPOTTER: Initializing UI...")


	audioSpinner = ac.addSpinner (app, "Audio")
	audioLabel = ac.addLabel (app, "{}".format(audio))
	audioVolSpinner = ac.addSpinner (app, "Volume")

	enableCheck = ac.addCheckBox (app, "Enable Spotter")
	replayEnableCheck = ac.addCheckBox (app, "Enabled in Replays")

	ac.setSize(app, 300, 220)

	ac.setPosition(enableCheck,60,50)
	ac.setValue(enableCheck, USEnabled)
	ac.addOnCheckBoxChanged(enableCheck,onEnableCheck)

	ac.setPosition(replayEnableCheck,60,100)
	ac.setValue(replayEnableCheck, USReplayEnabled)
	ac.addOnCheckBoxChanged(replayEnableCheck,onReplayEnableCheck)
	
	ac.setFontAlignment(audioLabel,"center")
	ac.setPosition(audioLabel,90,150)
	ac.setSize(audioSpinner,100,20)
	ac.setPosition(audioSpinner,40,150)

	audioList = os.listdir(os.path.join(os.path.dirname(__file__),"audio"))
	ac.setRange(audioSpinner,0,len(audioList)-1)
	ac.setStep(audioSpinner,1)
	#ac.setValue(audioSpinner,audioList.index(audio))
	ac.addOnValueChangeListener(audioSpinner,onAudioSpin)

	ac.setSize(audioVolSpinner,80,20)
	ac.setPosition(audioVolSpinner,180,150)
	ac.setStep(audioVolSpinner,1)
	ac.setRange(audioVolSpinner,1,10)
	ac.setValue(audioVolSpinner,audioVol)
	ac.addOnValueChangeListener(audioVolSpinner,onAudioVolSpin)
	ac.log("SPOTTER: UI Loaded")

def acUpdate(dt):
	global lapReset
	global minReset
	global secReset
	#speed = ac.getCarState(0, acsys.CS.SpeedKMH)
	#if speed > 105 and ac.getCarName(0) == "ks_toyota_ae86" and ac.isCameraOnBoard(0):
	#	sound.play(os.path.join(os.path.dirname(__file__), "audio//JJPack//n37.wav"))		
	#else:
	#	sound.stop()

	#racing with enabled or watching replay with replayenabled and enabled
	if (USEnabled and sim_info.graphics.status == 2) or (sim_info.graphics.status == 1 and USReplayEnabled and USEnabled):
		if ac.getCarState(0, acsys.CS.LapTime) > 0 and ac.getCarState(0, acsys.CS.LapTime) < 50 and lapReset == False and ac.getCarState(0,acsys.CS.LastLap) > 1000:
			lapReset = True
			sayTime ("m", ac.getCarState(0,acsys.CS.LastLap))
			#sayTime ("0")
		elif ac.getCarState(0,acsys.CS.LapTime) > 750 and ac.getCarState(0, acsys.CS.LapTime) < 800 and lapReset == True and minReset == False and ac.getCarState(0,acsys.CS.LastLap) > 1000:
			if (ac.getCarState(0,acsys.CS.LastLap)/1000)%60 < 10:
				sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS","0")))
			sayTime ("s",ac.getCarState(0,acsys.CS.LastLap))
			minReset = True

		elif ac.getCarState(0,acsys.CS.LapTime) > 2150 and ac.getCarState(0, acsys.CS.LapTime) < 2200 and lapReset == True and minReset == True and secReset == False and ac.getCarState(0,acsys.CS.LastLap) > 1000:
			secReset = True
			if random.choice((True, False)) and (ac.getCarState(0,acsys.CS.LastLap)/10)%100 > 10:
				sayTime ("ths",ac.getCarState(0,acsys.CS.LastLap))
			else:
				sayTime ("ts",ac.getCarState(0,acsys.CS.LastLap))
				sayTime ("hs",ac.getCarState(0,acsys.CS.LastLap))

		elif ac.getCarState(0,acsys.CS.LapTime) > 5000 and ac.getCarState(0, acsys.CS.LapTime) < 5100 and lapReset == True:
			lapReset = False
			secReset = False
			minReset = False
			

#def on_click_toggle(*args):
    # global beeperEnabled
   # beeperEnabled = True
    # beeperEnabled = not beeperEnabled
    # ac.setText(labelToggle, LABEL_TOGGLEBEEPER.format("on" if beeperEnabled else "off"))

def readAudio (section, toFind):
	config.read(os.path.join(os.path.dirname(__file__),"audio//JJPack//audio.ini"))
	return random.choice(config[section][toFind].split(","))

def sayTime (unit, time):
	#sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS","1")))
	#sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS","0")))
	#sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",time)))
	if unit == "m":
		#ac.log(str((time/(1000*60))%60))
		sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",str((time//(1000*60))%60))))
	elif unit == "s":
		#ac.log(str((time/1000)%60))
		sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",str((time//(1000))%60))))
	elif unit == "ths":
		#ac.log(str((time/10)%100))
		sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",str((time//10)%100))))
	elif unit == "ts":
		#ac.log(str((time/100)%10))
		sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",str((time//100)%10))))
	elif unit == "hs":
		#ac.log(str((time/10)%10))
		sound.queue(os.path.join(os.path.dirname(__file__), "audio//JJPack//" + readAudio("NUMBERS",str((time//10)%10))))

	#If you queue a sound while there's already one waiting to be played, it replaces the waiting one

	#sound.stop()

def readNum (number):
	return 0

def disable ():
	#turn off spotter
	saveConfig()

def saveConfig ():
	return 0

def onAudioSpin (val):
	return 0

def onAudioVolSpin (val):
	return 0

def onEnableCheck (label, val):
	return 0

def onReplayEnableCheck (label,val):
	return 0