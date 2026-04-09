import pygame as pg
import numpy as np
import sounddevice as sd
import scipy as sp
import matplotlib.pyplot as plt


pg.init()
pg.mixer.init()
screen = pg.display.set_mode((1280, 720))
font = pg.font.SysFont("Impact", 48)

class Button:
    def __init__():
        pass

note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
key_to_freq = {}
for key_number in range(36, 72):  # C2 (36) to B4 (71)
    octave = (key_number // 12) - 1
    note = note_names[key_number % 12] + str(octave)
    frequency = 440 * 2**((key_number - 69) / 12)
    key_to_freq[note] = round(frequency, 2)

pressed_keys = set()

def draw_keyboard():
    white_keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    black_keys = ['C#', 'D#', 'F#', 'G#', 'A#']
    white_key_width = 20
    white_key_height = 100
    black_key_width = 12
    black_key_height = 60
    keyboard_width = 21 * white_key_width
    keyboard_x = (1280 - keyboard_width) // 2
    base_y = 620
    pg.draw.rect(screen, (100, 200, 50), (0, 500, 1280, 300))

    white_positions = {}
    white_index = 0
    for i in range(36, 72):
        octave = (i // 12) - 1
        note = note_names[i % 12]
        if note in white_keys:
            key_id = f"{note}{octave}"
            x = keyboard_x + white_index * white_key_width
            white_positions[key_id] = x
            is_pressed = key_id in pressed_keys
            key_color = (180, 200, 255) if is_pressed else (255, 255, 255)
            pg.draw.rect(screen, key_color, (x, base_y, white_key_width, white_key_height))
            pg.draw.rect(screen, (0, 0, 0), (x, base_y, white_key_width, white_key_height), 1)
            white_index += 1

    for i in range(36, 72):
        octave = (i // 12) - 1
        note = note_names[i % 12]
        if note in black_keys:
            if note == 'C#':
                ref_note = f"C{octave}"
            elif note == 'D#':
                ref_note = f"D{octave}"
            elif note == 'F#':
                ref_note = f"F{octave}"
            elif note == 'G#':
                ref_note = f"G{octave}"
            elif note == 'A#':
                ref_note = f"A{octave}"
            key_id = f"{note}{octave}"
            x = white_positions[ref_note] + white_key_width - (black_key_width // 2)
            is_pressed = key_id in pressed_keys
            key_color = (80, 120, 255) if is_pressed else (0, 0, 0)
            pg.draw.rect(screen, key_color, (x, base_y, black_key_width, black_key_height))


def synth(frequency, duration=0.5,  sampling_rate=44100, apply_delay=True, sin_wave=True, square_wave=False, triangle_wave=False): #CHANGE DURATION TO BE BASED OFF A DIAL THAT CAN BE ADJUSTED IN THE GUI
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
        delay_samples = int(0.01 * sampling_rate) # CHANGE IT SO THE DELAY CAN BE ADJUSTED IN THE GUI
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
    screen.fill((0, 0, 0))  # Clear the screen each frame
    draw_keyboard()
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
                pressed_keys.add(note)
        if event.type == pg.KEYUP:
            key_name = pg.key.name(event.key)
            if key_name in key_to_note:
                note = key_to_note[key_name]
                if note in pressed_keys:
                    pressed_keys.remove(note)

    pg.display.flip()
