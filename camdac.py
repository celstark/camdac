from gpiozero import RotaryEncoder, Button
import signal
import sys
from camilladsp import CamillaClient


'''
Base code for the CamDAC

This lets you program your encoders and switchers to adjust features you'd like 
on the Camilla DSP. Key to this is that in your Camilla DSP yaml file, you have
defined a set of 5 filters called "Filt1", "Filt2" ... "Filt5" that you can
quickly tap into here. In truth, you can name them what you want in the YAML as
anything you put in here that isn't "Volume" or "VolBal" just gets passed into
Camilla

'''
# What does one click of a knob do for each control?
volume_step = 0.25
balance_step = 0.1
eq_step = 0.5

DEBUG = 1

########################## CUSTOMIZE UNLIKELY #############################
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
    
########################## CUSTOMIZE POSSIBLE #############################
# Setup your hardware 
#
# If you're using the stock 5-encoder setup, no need to customize this part
# There are some bits like bounce_time and max_steps (sets the resolution)
# that might be worth considering. If you're using different IO pins, this
# encpins has the format A, B, SW

encpins = [ [12,13,16],
            [7,5,6],
            [9,11,8],
            [24,25,10],
            [27,22,23]]

port = 1234 # What port is Camilla's server running on? 1234 is the default

# Setup the encoder and it's mode. 
#   max_steps: Sets the range of the encoder.  Steps go from -max_steps to +max_steps as you rotate. Our dB steps
#         are set by the global above. This prevents you from having to spin like crazy to undo any massive spins
#   bounce_time: Helps prevent double-clicks when pressing the encoder in.  Min time in sec to count as a press
#   name: IMPORTANT -- This can be "Volume", "VolBal", OR the name of a filter in your CamDSP_config.yml file
#         By default, you have Filt1-Filt5 in there.  In truth, it can be any named filter in the config.
#         Note, you can, of course, override these names below when you setup the event handlers. I've set this
#         up here to show how you can easily have them be defaults
knob1 = Encoder(
    RotaryEncoder(a=encpins[0][0], b=encpins[0][1], max_steps=64),
    Button(encpins[0][2], bounce_time = 0.1),
    name="VolBal" )

knob2 = Encoder(
    RotaryEncoder(a=encpins[1][0], b=encpins[1][1], max_steps=64),
    Button(encpins[1][2], bounce_time = 0.1),
    name="Filt1" )

knob3 = Encoder(
    RotaryEncoder(a=encpins[2][0], b=encpins[2][1], max_steps=64),
    Button(encpins[2][2], bounce_time = 0.1),
    name="Filt2" )

knob4= Encoder(
    RotaryEncoder(a=encpins[3][0], b=encpins[3][1], max_steps=64),
    Button(encpins[3][2], bounce_time = 0.1),
    name="Filt3" )

knob5 = Encoder(
    RotaryEncoder(a=encpins[4][0], b=encpins[4][1], max_steps=64),
    Button(encpins[4][2], bounce_time = 0.1),
    name="Filt4" )

########################## CUSTOMIZE UNLIKELY #############################
# Callback functions to actually do things
#
# Here, we define the funtions under the hood that happen when any knob is 
# turned or any button is pressed. Don't look here first for customization

def toggle_mode(dev, owner=None):
    # Sent but button events -- will swap the "mode" of the dial for that encoder
    print(f'Button toggle by hold -- before: val={owner.knob.value} steps={owner.knob.steps} devnum={dev.pin.number} name={owner.name}')
    owner.toggle_mode()
    print(f'                          after: val={owner.knob.value} steps={owner.knob.steps} devnum={dev.pin.number} name={owner.name}')

def adjust_knob(dev, dir=0, owner=None):
    # Top-level event handler for when a knob is rotated CW - calls appropriate function
    if DEBUG:
        print(f'INFO: Knob adjustment for {owner.name} of {dir}')
    if owner.name == "Volume":
        adjust_volume(dir)
    elif owner.name == "VolBal":
        if owner.mode == 0: 
            adjust_volume(dir)
        elif owner.mode == 1:
            adjust_balance(dev.steps)
    else:
        adjust_filter(owner,dir)

# Here, we send calls to Camilla
def adjust_volume(dir):
    if DEBUG:
        print(f'INFO: Adjusting volume by {volume_step * dir}')
    cdsp.volume.adjust_volume(0,volume_step * dir)

def adjust_balance(steps):
    # Running this in a relative mode to make sure it's spot on
    # Using encoder steps, not value here
    if steps == 0: # Set both faders to 0 dB
        if DEBUG:
            print(f'INFO: Resetting balance')
        cdsp.volume.set_volume(1,0) 
        cdsp.volume.set_volume(2,0)
    elif steps > 0: # Rightwards -- dial left down
        if DEBUG:
            print(f'INFO: Balance rightwards to {-1.0 * balance_step * steps} dB {steps}')
        cdsp.volume.set_volume(1, -1.0 * balance_step * steps)
        cdsp.volume.set_volume(2,0)
    elif steps < 0: # Leftwards -- 
        if DEBUG:
            print(f'INFO: Balance leftwards to {1.0 * balance_step * steps} dB {steps}')
        cdsp.volume.set_volume(2, 1.0 * balance_step * steps)
        cdsp.volume.set_volume(1,0)

def adjust_filter(owner, dir=0.0):
    # Using relative adjustments here
    tmp_conf = cdsp.config.active()
    filt_name=owner.name
    try:
        cur_gain = tmp_conf['filters'][filt_name]['parameters']['gain']
    except:
        print(f"ERROR - Cannot retrieve paramters for {filt_name}")
        return
    new_gain = cur_gain + eq_step * dir
    if DEBUG:
        print(f"INFO: Adjusting {filt_name} from {cur_gain} dB to {new_gain} dB  [{tmp_conf['filters'][filt_name]['parameters']['freq']} Hz Q={tmp_conf['filters'][filt_name]['parameters']['q']} ]")
    tmp_conf['filters'][filt_name]['parameters']['gain'] = new_gain
    cdsp.config.set_active(tmp_conf)
    
########################## CUSTOMIZE LIKELY #############################
# Setup what the knobs and buttons actually do
#
# Let's make knob1 a volume/balance knob. We don't really need to set the name here as
# it was set by default above.  But, I'm just showing an over-ride here
knob1.name="VolBal"
knob1.knob.when_rotated_clockwise = lambda: adjust_knob(knob1.knob, 1, knob1)
knob1.knob.when_rotated_counter_clockwise = lambda: adjust_knob(knob1.knob, -1, knob1)
knob1.button.when_pressed = lambda: toggle_mode(knob1.button, knob1)

# Let's keep knobs 2-4 to be Filt1-3 and their buttons do nothing. But, we'll still
# setup the event handler to call adjust_knob, let it know the direction, and the owner
knob2.knob.when_rotated_clockwise = lambda: adjust_knob(knob2.knob, 1, knob2)
knob2.knob.when_rotated_counter_clockwise = lambda: adjust_knob(knob2.knob, -1, knob2)

knob3.knob.when_rotated_clockwise = lambda: adjust_knob(knob3.knob, 1, knob3)
knob3.knob.when_rotated_counter_clockwise = lambda: adjust_knob(knob3.knob, -1, knob3)

knob4.knob.when_rotated_clockwise = lambda: adjust_knob(knob4.knob, 1, knob4)
knob4.knob.when_rotated_counter_clockwise = lambda: adjust_knob(knob4.knob, -1, knob4)

# But, let's have knob 5 be Filt5 as an override
knob5.name="Filt5"
knob5.knob.when_rotated_clockwise = lambda: adjust_knob(knob5.knob, 1, knob5)
knob5.knob.when_rotated_counter_clockwise = lambda: adjust_knob(knob5.knob, -1, knob5)


######################## CUSTOMIZE UNLIKELY #########################
# Connect to Camilla
try:
    cdsp = CamillaClient("127.0.0.1",port)
    cdsp.connect()
except:
    print("Issue connecting to CamillaDSP")
    sys.exit()
signal.pause()
