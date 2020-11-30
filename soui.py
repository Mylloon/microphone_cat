import numpy as np
import sounddevice as sd
from time import sleep
from tkinter import Tk, Canvas, Label, PhotoImage

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
        self.speaking = "speaking.png"
        self.notspeaking = "not_speaking.png"

    def refresh(self):
        self.canvas.itemconfig(self.canvas_image, image = PhotoImage(master = self.fenetre, file = self.get_image()))
        self.fenetre.update_idletasks()
        self.fenetre.after(self.buffer, self.refresh)

    def get_image(self):
        if Microphone().get_status_speaking():
            print("parle")
            return self.speaking
        else:
            print("parle pas")
            return self.notspeaking
    
    def start(self):
        self.fenetre = Tk()
        self.fenetre.title('Microphone')
        self.canvas = Canvas(self.fenetre)
        self.canvas.configure(width = 1080, height = 2140)
        self.canvas_image = self.canvas.create_image(540, 1070, image = PhotoImage(master = self.fenetre, file = self.get_image()))
        
        self.refresh()

        self.fenetre.mainloop()

if __name__ == '__main__':
    Affichage().start()
