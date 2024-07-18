import tkinter as tk
from tkinter import filedialog
import pygame
import os
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import threading

pygame.mixer.init()

is_playing = False
current_audio = None

def cargar_y_play():
    global is_playing, current_audio
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    if filepath:
        current_audio = AudioSegment.from_file(filepath)
        song_label.config(text=os.path.basename(filepath))
        is_playing = True
        threading.Thread(target=play_audio).start()
        visualizar()

def play_audio():
    global is_playing
    if current_audio:
        play(current_audio)
    is_playing = False

def detener():
    global is_playing
    pygame.mixer.music.stop()
    song_label.config(text="No se ha cargado ninguna canción")
    is_playing = False


root = tk.Tk()
root.title("XPlayer")
root.geometry("800x600")

frame_visual = tk.Frame(root, bg='black', width=800, height=300)
frame_visual.pack_propagate(False)
frame_visual.pack()

canvas = tk.Canvas(frame_visual, width=800, height=300)
canvas.pack()


os.environ['SDL_WINDOWID'] = str(canvas.winfo_id())
pygame.display.init()
screen = pygame.display.set_mode((800, 300))

frame_controls = tk.Frame(root)
frame_controls.pack(fill=tk.BOTH, expand=True)

control_frame = tk.Frame(frame_controls)
control_frame.pack(side=tk.LEFT, padx=20, pady=20)

play_button = tk.Button(control_frame, text="Cargar y Reproducir", command=cargar_y_play)
play_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(control_frame, text="Detener", command=detener)
stop_button.pack(side=tk.LEFT, padx=5)


playlist_frame = tk.Frame(frame_controls)
playlist_frame.pack(side=tk.RIGHT, padx=20, pady=20)

playlist_label = tk.Label(playlist_frame, text="Lista de Reproducción")
playlist_label.pack()

playlist_box = tk.Listbox(playlist_frame, width=40)
playlist_box.pack()

song_label = tk.Label(root, text="No se ha cargado ninguna canción")
song_label.pack()

def visualizar():
    if is_playing:
        screen.fill((0, 0, 0))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                root.quit()

        pygame.draw.circle(screen, (0, 255, 0), (400, 150), np.random.randint(50, 150))
        pygame.draw.rect(screen, (255, 0, 0), (np.random.randint(0, 700), np.random.randint(0, 200), 100, 100))
        
        pygame.display.update()
        root.after(100, visualizar)  

root.mainloop()
