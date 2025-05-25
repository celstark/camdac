from gpiozero import RotaryEncoder, Button
from signal import pause  # one way to nicely not exit
from camilladsp import CamillaClient
import sys

# This is not actual code ... it's a playground


# see also the done.wait() from here: https://gpiozero.readthedocs.io/en/stable/recipes.html#rotary-encoder


port = 1234 # Seems to be the default


knob1 = RotaryEncoder(a=12, b=13, max_steps=64)  # Give us 64 possible levels for starters
knob2 = RotaryEncoder(a=7, b=5, max_steps=64)
knob3 = RotaryEncoder(a=9, b=11, max_steps=64)
button1 = Button(16,bounce_time=0.1)
button2 = Button(6,bounce_time=0.1)
button3 = Button(8,bounce_time=0.1)
button4 = Button(10,bounce_time=0.1)

# Initialize the rotary encoder's SW pin on GPIO pin 22
#button = Button(22)

cur_knob1 = 0  # This isn't in any real units -- just steps
cur_knob2 = 0

def knob1_adjust_param(): 
    # Tester for what to do when knob is adjusted
    global cur_knob1

    adjustment = (knob1.steps - cur_knob1) * 0.5
    cur_knob1 = knob1.steps
    cur_vol=cdsp.volume.volume(0)
    cdsp.volume.adjust_volume(0,adjustment)
    new_vol=cdsp.volume.volume(0)
    print(f'Vol change: ',cur_knob1,adjustment,knob1.steps,cur_vol,new_vol)

def knob2_adjust_param(): 
    global cur_knob2

    tmp_conf = cdsp.config.active()
    print(tmp_conf['filters']['LShelf']['parameters'])
    cur_gain = tmp_conf['filters']['LShelf']['parameters']['gain']
    adjustment = (knob2.steps - cur_knob2) * 0.5
    cur_knob2 = knob2.steps
    tmp_conf['filters']['LShelf']['parameters']['gain'] = cur_gain + adjustment
    cdsp.config.set_active(tmp_conf)
    print(f'Shelf change: ',cur_knob1,adjustment,cur_gain,cur_gain+adjustment)

def button1_press():
    print('Button on knob 1')

def button2_press():
    print('Button on knob 2')

def button_press(dev):
    # Testing parameters in the event handlers...
    print(f'Button: val={dev.value}  devnum={dev.pin.number}')

def knob_adjust_param(dev):
    # Testing parameters in the event handlers...
    print(f'Knob: steps={dev.steps}  val={dev.value}   devnum={dev.a.pin} {dev.b.pin}')



button1.when_pressed = button1_press
button2.when_pressed = button2_press
button3.when_pressed = button_press
button4.when_pressed = button_press

knob1.when_rotated = knob1_adjust_param
knob2.when_rotated = knob2_adjust_param
knob3.when_rotated = knob_adjust_param
print(dir(knob3))

try:
    cdsp = CamillaClient("127.0.0.1",port)
    cdsp.connect()
except:
    print("Issue connecting to CamillaDSP")
    sys.exit()

knob1.when_rotated = knob1_adjust_param
knob2.when_rotated = knob2_adjust_param

cur_conf = cdsp.config.active()
print(cur_conf['filters'])

pause()