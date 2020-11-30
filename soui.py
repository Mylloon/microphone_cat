import numpy as np
import sounddevice as sd
from time import sleep
from tkinter import Tk, Canvas, Label, PhotoImage

class Microphone:

    def __init__(self):
        self.speaking = False

    def audio_callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if int(volume_norm) > 2:
            self.speaking = True
        elif int(volume_norm) < 2:
            self.speaking = False

    def get_status_speaking(self):
        return self.speaking

    def start(self):
        with sd.InputStream(callback = self.audio_callback):
            Affichage().start()

class Affichage:

    def __init__(self):
        self.buffer = 500 # milliseconds
        self.speaking = "speaking.png"
        self.notspeaking = "not_speaking.png"

    def refresh(self):
        self.get_image()
        self.label.config(image = self.img)
        self.fenetre.update_idletasks()
        self.fenetre.after(self.buffer, self.refresh)

    def get_image(self):
        if Microphone().get_status_speaking():
            print("parle")
            self.img = PhotoImage(file = self.speaking)
        else:
            self.img = PhotoImage(file = self.notspeaking)
    
    def start(self):
        self.fenetre = Tk()
        self.fenetre.title('Microphone')
        self.fenetre.geometry("357x697")
        self.get_image()
        self.label = Label(self.fenetre, image = self.img)
        self.label.pack(fill = "both", expand = "yes")
        
        self.refresh()

        self.fenetre.mainloop()

if __name__ == '__main__':
    Microphone().start()
