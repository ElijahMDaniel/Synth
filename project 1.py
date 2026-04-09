import pygame as pg
import numpy as np
import sounddevice as sd
import scipy as sp

pg.init()
pg.mixer.init()
screen = pg.display.set_mode((1280, 720))
font = pg.font.SysFont("Impact", 48)

class Button:
    def __init__()

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_to_freq = {}
for key_number in range(36, 72):  # C2 (36) to B4 (71)
    octave = (key_number // 12) - 1
    note = note_names[key_number % 12] + str(octave)
    frequency = 440 * 2**((key_number - 69) / 12)
    key_to_freq[note] = round(frequency, 2)

def synth(frequency, duration=0.5, sampling_rate=44100, apply_delay=True, sin_wave=True, square_wave=False, triangle_wave=False): #CHANGE DURATION TO BE BASED OFF A DIAL THAT CAN BE ADJUSTED IN THE GUI
    frames = int(duration*sampling_rate)
    # Default waveform if no flag is enabled
    arr = np.sin(2*np.pi*frequency*np.linspace(0, duration, frames))
    if sin_wave:
        arr = np.cos(2*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr + np.cos(4*np.pi*frequency*np.linspace(0,duration, frames))
        arr = arr - np.cos(6*np.pi*frequency*np.linspace(0,duration, frames))
    if square_wave:
        t = np.linspace(0, duration, frames)
        arr = np.sign(np.sin(2 * np.pi * frequency * t))
    if triangle_wave:
        t = np.linspace(0, duration, frames)
        arr = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t))
    if apply_delay: # ALLOW TOGGLE DELAY ON AND OFF WITH A CHECKBOX IN THE GUI
        delay_samples = int(0.1 * sampling_rate) # CHANGE IT SO THE DELAY CAN BE ADJUSTED IN THE GUI
        delayed_arr = np.zeros_like(arr)
        delayed_arr[delay_samples:] = arr[:-delay_samples] * 0.5 #ALLOW DELAY VOLUME TO BE ADJUSTED IN THE GUI
        arr = arr + delayed_arr
        arr = np.clip(arr, -1, 1)  # Prevent clipping

    sound = np.asarray([32767*arr,32767*arr]).T.astype(np.int16)
    sound = pg.sndarray.make_sound(sound.copy())
    return sound

keyslist = '1234567890-=qwertyuiop[]asdfghjkl;\'z' #C2 to B2 is 1234567890-=, C3 to B3 is qwertyuiop[], C4 to B4 is asdfghjkl;'z

note_list = list(key_to_freq.keys())
key_to_note = {keyslist[i]: note_list[i] for i in range(min(len(keyslist), len(note_list)))}

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            key_name = pg.key.name(event.key)
            if key_name in key_to_note:
                note = key_to_note[key_name]
                freq = key_to_freq[note]
                sound = synth(freq)
                sound.set_volume(0.3)  # Decrease volume to 30%
                sound.play()
                print(f"Playing {note}")

    pg.display.flip() 
