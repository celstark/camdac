from gpiozero import RotaryEncoder, Button
import signal
import sys

'''
Simple tester to make sure all the knobs are wired up correctly
~/camilladsp/.venv/bin/python encoder_tester.py

Either hold a button for >1s or ctrl-c to exit

'''

encpins = [ [12,13,16],
            [7,5,6],
            [9,11,8],
            [24,25,10],
            [27,22,23]]

knob1 = RotaryEncoder(a=encpins[0][0], b=encpins[0][1], max_steps=64)
button1 = Button(encpins[0][2])
knob2 = RotaryEncoder(a=encpins[1][0], b=encpins[1][1], max_steps=64)
button2 = Button(encpins[1][2])
knob3 = RotaryEncoder(a=encpins[2][0], b=encpins[2][1], max_steps=64)
button3 = Button(encpins[2][2])
knob4 = RotaryEncoder(a=encpins[3][0], b=encpins[3][1], max_steps=64)
button4 = Button(encpins[3][2])
knob5 = RotaryEncoder(a=encpins[4][0], b=encpins[4][1], max_steps=64)
button5 = Button(encpins[4][2])


def knob1_adjust(): 
    print(f'Knob 1  {knob1.steps}')
def knob2_adjust(): 
    print(f'Knob 2  {knob2.steps}')
def knob3_adjust(): 
    print(f'Knob 3  {knob3.steps}')
def knob4_adjust(): 
    print(f'Knob 4  {knob4.steps}')
def knob5_adjust(): 
    print(f'Knob 5  {knob5.steps}')

def button1_press():
    print('Button 1 press')
def button2_press():
    print('Button 2 press')
def button3_press():
    print('Button 3 press')
def button4_press():
    print('Button 4 press')
def button5_press():
    print('Button 5 press')

def button_hold():
    print('Exiting')
    signal.raise_signal(signal.SIGHUP)  # Alt is done.set() here


button1.when_pressed = button1_press
button2.when_pressed = button2_press
button3.when_pressed = button3_press
button4.when_pressed = button4_press
button5.when_pressed = button5_press

button1.when_held = button_hold
button2.when_held = button_hold
button3.when_held = button_hold
button4.when_held = button_hold
button5.when_held = button_hold

knob1.when_rotated = knob1_adjust
knob2.when_rotated = knob2_adjust
knob3.when_rotated = knob3_adjust
knob4.when_rotated = knob4_adjust
knob5.when_rotated = knob5_adjust

signal.pause()  # This could also have 'done' be an Event() and here call done.wait()