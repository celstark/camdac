from gpiozero import RotaryEncoder, Button
import signal
import sys

'''
Simple tester to make sure all the knobs are wired up correctly
~/camilladsp/.venv/bin/python encoder_tester.py

Either hold Button1 for >1s or ctrl-c to exit

'''

encpins = [ [12,13,16],
            [7,5,6],
            [9,11,8],
            [24,25,10],
            [27,22,23]]

# Setup a simple class for our encoders
class Encoder:
    def __init__(self,knob, button, mode=0, name=None):
        self.knob=knob
        self.button=button
        self.mode=mode
        self.name=name
        self.steps_last = [0, 0]  # We use these to allow the button to toggle modes
        self.val_last = [0.0, 0.0]
    
    def toggle_mode(self):
        # store the current readings
        self.steps_last[self.mode]=self.knob.steps
        self.val_last[self.mode]=self.knob.steps
        # toggle the mode
        if self.mode:
            self.mode=0
        else:
            self.mode=1
        # bring in the other mode values -- we actually only need to change one as it updates the other
        self.knob.steps=self.steps_last[self.mode]
    
knob1 = Encoder(
    RotaryEncoder(a=encpins[0][0], b=encpins[0][1], max_steps=64),
    Button(encpins[0][2], bounce_time = 0.1),
    name="Knob 1" )

knob2 = Encoder(
    RotaryEncoder(a=encpins[1][0], b=encpins[1][1], max_steps=64),
    Button(encpins[1][2], bounce_time = 0.1),
    name="Knob 2" )

knob3 = Encoder(
    RotaryEncoder(a=encpins[2][0], b=encpins[2][1], max_steps=64),
    Button(encpins[2][2], bounce_time = 0.1),
    name="Knob 3" )

knob4= Encoder(
    RotaryEncoder(a=encpins[3][0], b=encpins[3][1], max_steps=64),
    Button(encpins[3][2], bounce_time = 0.1),
    name="Knob 4" )

knob5 = Encoder(
    RotaryEncoder(a=encpins[4][0], b=encpins[4][1], max_steps=64),
    Button(encpins[4][2], bounce_time = 0.1),
    name="Knob 5" )



def knob_adjust(dev): 
    print(f'Knob: steps={dev.steps}  val={dev.value}   devnum={dev.a.pin} {dev.b.pin}')
    
def button_press(dev):
    print(f'Button: val={dev.value}  devnum={dev.pin.number}')    

def button_exit():
    print('Exiting')
    signal.raise_signal(signal.SIGHUP)  # Alt is done.set() here

def toggle_mode(dev, owner=None):
    print(f'Button toggle by hold -- before: val={owner.knob.value} steps={owner.knob.steps} devnum={dev.pin.number} name={owner.name}')
    owner.toggle_mode()
    print(f'                          after: val={owner.knob.value} steps={owner.knob.steps} devnum={dev.pin.number} name={owner.name}')
    
    

knob1.button.when_held = button_exit
knob1.button.when_pressed = button_press
knob1.knob.when_rotated = knob_adjust

knob2.button.when_pressed = button_press
knob2.knob.when_rotated = knob_adjust

knob3.button.when_pressed = button_press
knob3.knob.when_rotated = knob_adjust

knob4.button.when_pressed = button_press
knob4.knob.when_rotated = knob_adjust

knob5.button.when_pressed = button_press
knob5.button.when_held=lambda: toggle_mode(knob5.button, knob5)
knob5.knob.when_rotated = knob_adjust

signal.pause()  # This could also have 'done' be an Event() and here call done.wait()