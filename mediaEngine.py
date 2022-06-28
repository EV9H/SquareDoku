import pygame as p
import random
class MusicPlayer:

    def __init__(self):
        self.BGM_VOLUME = 1
        self.FX_VOLUME = 0.7
        self.mixer = p.mixer
        self.mixer.pre_init(frequency=44100, size=-16, channels=5, buffer=4096)
        self.mixer.init()
        self.music = {"b1": p.mixer.music.load("Music/floatingPointsLastBloom.wav")}
        self.sound = {"p1": p.mixer.Sound("Music/p1.wav"), "p2": p.mixer.Sound("Music/p2.ogg"), "p3": p.mixer.Sound("Music/p3.ogg"), "p4": p.mixer.Sound("Music/p4.ogg"),
                      "s1": p.mixer.Sound("Music/s1.ogg"), "s2": p.mixer.Sound("Music/s2.ogg"),"s3": p.mixer.Sound("Music/s3.ogg"),
                      "e1": p.mixer.Sound("Music/e1.ogg"),"e2": p.mixer.Sound("Music/e2.ogg"), "e3": p.mixer.Sound("Music/e3.ogg"), "e4": p.mixer.Sound("Music/e4.ogg")}
        self.countdownSound = p.mixer.Sound("Music/countdown1.ogg")
        self.countdownChannel = p.mixer.Channel(0)
        self.fxChannel = p.mixer.Channel(1)
        self.placementCnt = 1

    def playBg(self):
        p.mixer.music.set_volume(self.BGM_VOLUME)
        p.mixer.music.play(-1,fade_ms=1)

    def stopBg(self):
        p.mixer.music.stop()

    def playPlacementSound(self):
        if(self.placementCnt > 4):
            self.placementCnt = 1
        soundName = "p" + str(self.placementCnt)
        self.sound[soundName].set_volume(self.FX_VOLUME)
        self.sound[soundName].play(fade_ms= 500)
        self.placementCnt += 1

    def playSelectSound(self):
        choice = random.randint(1,3)
        soundName = "s" + str(choice)
        self.sound[soundName].set_volume(self.FX_VOLUME)
        self.sound[soundName].play(fade_ms= 500)
        self.sound[soundName].play(fade_ms=500)

    def playEraseSound(self, degree): # degree = 1 ~ 4
        soundName = "e"+str(degree)
        self.sound[soundName].set_volume(self.FX_VOLUME)
        self.sound[soundName].play(fade_ms= 500)



    def playCountdown(self):
        self.countdownChannel.play(self.countdownSound)
        self.countdownChannel.set_volume(self.FX_VOLUME)

    def stopCountdown(self):
        self.countdownChannel.stop()