from threading import Thread, Event
import winsound
import ac, acsys


class SoundPlayer(object):
    def __init__(self, filename):
        ac.log ("SPOTTER: Initializing SoundPlayer...")
        self.filename = filename
        self.almost = filename
        self._play_event = Event()
        self.thread = Thread(target=self._worker)
        self.thread.daemon = True
        self._audio_cache = {}
        self.waiting = False
        self.ready = False
        self._wait_event = Event()
        self.waitThread = Thread(target=self._waiter)
        self.waitThread.daemon = True


        self.thread.start()
        self.waitThread.start()

        ac.log ("SPOTTER: SoudPlayer Loaded")

    def queue(self,filename=None):
        if filename is not None:
            ac.log("SPOTTER: "+filename+" was queued")
            self.almost = filename
            self._wait_event.set()


    
    #def play(self, filename=None):
    #    if filename is not None:
    #        self.filename = filename
    #    self._play_event.set()
    
    def stop(self):
        self._wait_event.clear()
        self._play_event.clear()
        self.waiting = False

    def _waiter(self):
        while True:
            self._wait_event.wait()
            if self.waiting == True and self._play_event.isSet():
                self._play_event.clear()
                self._wait_event.clear()
                self.ready = True
            elif self.waiting == False:
                self.waiting = True
                self.ready = False
                self.filename = self.almost
                self._play_event.set()
                self._wait_event.clear()



    def _worker(self):
        while True:
            self._play_event.wait()
            self.waiting = True
            ac.log("SPOTTER: playing "+self.filename)
            try:
                winsound.PlaySound(self.filename, winsound.SND_FILENAME)
            except Exception:
                ac.log ("SPOTTER: Error playing " + self.filename)
            self.waiting = False
            #ac.log("TIME: "+ str(ac.getCarState(0,acsys.CS.LapTime)))
            self._play_event.clear()
            if self.ready:
                self.ready = False
                self._wait_event.set()
