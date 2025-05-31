
# Case to improve
- You need to remove the SD card to get the board in and out.  1 mm more and we'd clear
- Different knobs, 4 controls, or a bit bigger case -- it's a bit cramped

# Software to-do
- Getting clicks between tracks at least with Shairplay. (Seems to be tied to the DAC HAT)
- Handle offset / pre-amp gain. Right now, the main Volume knob handles this but we could limit it or use the Aux ones I'm using for balance to ensure you never go above -X dB. (Pipeline goes resampler, master volume, PEQ knob filters, balance, fixed PEQ filters)
- Run `camdac.py` as a service
- Add ability to re-define filters more easily
- Setup better handling of multiple bit rates

# Hardware to-do
- ~~USB "gadget" mode for inline digital PEQ~~

-----------
Desktop audio not working -- https://github.com/HEnquist/camilladsp-config
- Put their asound.conf into /etc/
- 

