import numpy as np
import sounddevice as sd
from time import sleep
from tkinter import Tk, Label, PhotoImage

class Microphone:

    def __init__(self):
        self.buffer = 0.1 # seconds
        self.speaking = False

    def audio_callback(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if int(volume_norm) > 2 and not self.speaking:
            self.speaking = True
        elif int(volume_norm) < 2 and self.speaking:
            self.speaking = False

    def get_status_speaking(self):
        return self.speaking

    def repeat(self):
        print(self.speaking)
        sleep(self.buffer)
        return self.repeat()

    def start(self):
        with sd.InputStream(callback = self.audio_callback):
            self.repeat()

class Affichage:

    def __init__(self):
        self.buffer = 500 # milliseconds
        self.speaking = "speaking.jpg"
        self.notspeaking = "not_speaking.jpg"

    def refresh(self):
        if Microphone().get_status_speaking():
            self.image.config(PhotoImage(file = self.speaking))
        else:
            self.image.config(PhotoImage(file = self.notspeaking))
        self.fenetre.update_idletasks()
        self.fenetre.after(self.buffer, self.refresh)
    
    def start(self):
        self.fenetre = Tk()
        self.fenetre.title('Microphone')
        self.image = Label(self.fenetre)
        self.image.pack()
        
        self.refresh()

        self.fenetre.mainloop()

if __name__ == '__main__':
    Affichage().start()
