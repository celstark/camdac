# Pinout

## Pins in use
The IQAudio / [Raspberry Pi branded DACs](https://www.raspberrypi.com/documentation/accessories/audio.html) all use GPIO 2 (SDA / I2C), 3 (SCL / I2C), and 18-21 (I2S). For the DAC PRO and DAC+, the rest are open. For the DigiAMP+ or Codec, they also use 22 (mute / unmute), 22 & 23 (rotary encoder or LED), 25 (IR sensor), and 27 (switch).  The Codec really doesn't seem to apply to this project, but the DigiAMP+ board might be used. So, if you're using the *DigiAMP+ (or another board) revisit the default IO piols*.

## Pins open
After this, though, we should have 17 pins open to us: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 22, 23, 24, 25, 26, and 27. If you do a full rotary-encoder + switch setup, you need 3 pins per encoder (2 for the encoder and 1 for the switch) meaning you can have 5 encoders going and still have 2 IO pins left for LED indicators (e.g., showing the mode a switch is in) or something else. 

## Default assignment
To simplify the wiring a bit, for the 5-encoder + switch version I've grouped things for the GPIO prototype breadboard HAT I picked up as follows (A, B, _SW_):
1) 12, 13, _16_
2) 7 (CE1), 5, _6_
3) 9 (MISO), 11 (CLK), _8_ (CE0)
4) 24, 25, _10 (MOSI)_
5) 27, 22, _23_

So, in the code, for example, the right-most encoder knob, #5, uses pins 27 (A) and 22 (B) for the dial and 23 for the switch.

## I2C
Note, we can use the same I2C lines that the DAC is using for an optional display

# Resistors and wiring
We can likely get away without using pull-up resistors and just make sure the internal ones are enabled. The Pi has ~50k resistors baked into it, but its input impedance isn't far off that. For "strong" setting of the IO pins capable of working in noisy environments (e.g., with longer cable runs), you may want the resistor to be a tenth the input impedance and the internal ones are closer then to 1:1.  Ignoring them does simplify the hardware a touch as the board I picked does make including them not very elegant. Note, if you use modules rather than raw encoders, these typically have 10k resistors going between the Vcc and the junction between the data lines (CLK, DT, and SW) and their respective switches (the other end of each switch is on GND). Thus, the modules, are in a pull-up state and when the switches close, it gets pulled down.

But, here, we're going to go with using the internal ones. The `gpiozero` library has the default `pull_up` as True for buttons (wanting you to wire one end to the GPIO and the other to GND) -- i.e., it's engaging the internal pull-up resistors unless you manually set the `pull_up` paramter to _floating_.  For the rotary encoders, it expects the "A" and "B" data pins to go to GPIO and the "C" (common) to go to GND.  For any LEDs you choose, put something like a 300Ω resistor in series with it to limit the current and then directly hook it between the GPIO data line and GND.

If using basic encoders (non-modules):
- Solder a wire to the "A" terminal (leftmost of the 3 if looking from the front) and hook to the first number above
- Solder a wire to the "B" terminal (rightmost of the 3 if looking from the front) and hook to the second number above
- Strip ~2cm off another wire and use that to connect the "C" terminal (middle of the 3) and one side of the switch (either of the 2) thus jumpering them on the encoder end. Bring that wire and hook to the ground bus
- Solder a wire to the other end of the switch (the one you didn't jumper above) and hook that to the third number above.




