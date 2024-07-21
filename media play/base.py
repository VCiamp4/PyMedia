import tkinter as tk
from tkinter import filedialog
import pygame
import os
import numpy as np
import threading
import time


pygame.mixer.init()


is_playing = False
audio_duration = 0
start_time = 0
paused = False
pause_time = 0


temp_folder = "C:\\temp\\"
os.makedirs(temp_folder, exist_ok=True)
os.environ['TEMP'] = temp_folder

def cargar_y_play():
    global is_playing, audio_duration, start_time, paused
    filepath = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    if filepath:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        audio_duration = pygame.mixer.Sound(filepath).get_length()
        song_label.config(text=os.path.basename(filepath))
        is_playing = True
        paused = False
        start_time = time.time()
        visualizar()
        update_progress()
        scroll_text()

def detener():
    global is_playing
    pygame.mixer.music.stop()
    song_label.config(text="No se ha cargado ninguna canción")
    is_playing = False

def pausar():
    global paused, pause_time
    if not paused:
        pygame.mixer.music.pause()
        pause_time = time.time()
        paused = True


def continuar():
    global paused, start_time
    if paused:
        pygame.mixer.music.unpause()
        start_time += time.time() - pause_time
        paused = False
        update_progress()
        scroll_text()

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

pause_button = tk.Button(control_frame, text="Pausar", command=pausar)
pause_button.pack(side=tk.LEFT, padx=5)

resume_button = tk.Button(control_frame, text="Continuar", command=continuar)
resume_button.pack(side=tk.LEFT, padx=5)


playlist_frame = tk.Frame(frame_controls)
playlist_frame.pack(side=tk.RIGHT, padx=20, pady=20)

playlist_label = tk.Label(playlist_frame, text="Lista de Reproducción")
playlist_label.pack()

playlist_box = tk.Listbox(playlist_frame, width=40)
playlist_box.pack()


song_label = tk.Label(root, text="No se ha cargado ninguna canción")
song_label.pack()


time_passed_label = tk.Label(root, text="00:00")
time_passed_label.pack(side=tk.LEFT, padx=10)

time_remaining_label = tk.Label(root, text="00:00")
time_remaining_label.pack(side=tk.RIGHT, padx=10)


progress = tk.DoubleVar()
progress_bar = tk.Scale(root, variable=progress, orient="horizontal", length=700, from_=0, to=100, showvalue=0)
progress_bar.pack()


text_x = 800
scroll_speed = 2


def update_progress():
    if is_playing and not paused:
        elapsed_time = time.time() - start_time
        progress.set((elapsed_time / audio_duration) * 100)
        time_passed_label.config(text=time.strftime('%M:%S', time.gmtime(elapsed_time)))
        time_remaining_label.config(text=time.strftime('%M:%S', time.gmtime(audio_duration)))
        if elapsed_time < audio_duration:
            root.after(100, update_progress)
        else:
            detener()


def scroll_text():
    global text_x
    if is_playing and not paused:
        text_x -= scroll_speed
        if text_x < -song_label.winfo_width():
            text_x = 800
        song_label.place(x=text_x, y=300)  
        root.after(50, scroll_text)


def visualizar():
    if is_playing and not paused:
        screen.fill((0, 0, 0))  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                root.quit()


        pygame.draw.circle(screen, (0, 255, 0), (400, 150), np.random.randint(50, 150))
        pygame.draw.rect(screen, (255, 0, 0), (np.random.randint(0, 700), np.random.randint(0, 200), 100, 100))
        
        pygame.display.update()
        root.after(100, visualizar)  


root.mainloop()
