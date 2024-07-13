import tkinter as tk
from tkinter import filedialog
import pygame
import os

pygame.mixer.init()

def cargar_y_play():
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    if filepath:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        song_label.config(text=os.path.basename(filepath))
    
    #ventana principal 
    root = tk.Tk()
    root.title ("XPlayer")


    play_button = tk.button(root, text="Cargar y reproducir", command=cargar_y_play)
    play_button.pack()

    song_label = tk.Label(root, text="No se ha cargado ninguna canción")
    song_label.pack()

    # Iniciar el bucle de la interfaz de usuario
    root.mainloop()