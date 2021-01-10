import numpy as np
import sounddevice as sd
from time import sleep, time
from tkinter import Tk, Canvas, Label, PhotoImage
from PIL import Image

speaking = False

class Microphone:

    def audio_callback(self, indata, frames, time, status):
        global speaking
        volume_norm = np.linalg.norm(indata) * 10
        if int(volume_norm) > 2 and speaking == False:
            speaking = True
        elif int(volume_norm) < 2 and speaking == True:
            speaking = False

    def get_status_speaking(self):
        return speaking

    def start(self):
        with sd.InputStream(callback = self.audio_callback):
            Affichage().start()

class Affichage:

    def __init__(self):
        self.buffer = 100 # milliseconds
        self.speaking = "speaking.png"
        self.notspeaking = "not_speaking.png"
        self.whatamispeakingactually = self.notspeaking
        self.amispeaking = False

    def get_ratio_img(self):
        image = Image.open(self.speaking)
        image2 = Image.open(self.notspeaking)
        width, height = image.size
        width2, height2 = image2.size
        if width != width2 or height != height2:
            return None
        else:
            return f"{width}x{height}"

    def refresh(self):
        self.get_image()
        self.label.config(image = self.img)
        self.fenetre.update_idletasks()
        self.fenetre.after(self.buffer, self.refresh)

    def get_image(self):
        if Microphone().get_status_speaking():
            if self.amispeaking == False:
                self.amispeaking = True
                self.whatamispeakingactually = self.speaking
                self.img = PhotoImage(file = self.speaking)
                self.flash()
        else:
            self.amispeaking = False
            self.whatamispeakingactually = self.notspeaking
            self.img = PhotoImage(file = self.notspeaking)
    
    def flash(self):
        if self.amispeaking == True:
            if self.whatamispeakingactually == self.notspeaking:
                self.whatamispeakingactually = self.speaking
                self.img = PhotoImage(file = self.speaking)
            else:
                self.whatamispeakingactually = self.notspeaking
                self.img = PhotoImage(file = self.notspeaking)
            self.fenetre.after(self.buffer, self.flash)

    def start(self):
        self.fenetre = Tk()
        self.fenetre.title('Microphone')
        geo = self.get_ratio_img()
        if not geo:
            raise NameError("Sorry, images speaking and not_speaking don't have same ratio")
        self.fenetre.geometry(geo)
        self.fenetre.resizable(0, 0)
        self.get_image()
        self.label = Label(self.fenetre, image = self.img)
        self.label.pack(fill = "both", expand = "yes")
        
        self.refresh()

        self.fenetre.mainloop()

if __name__ == '__main__':
    Microphone().start()
