# camdac
DSP / DAC and headphone amplifier based on a Raspberry Pi and CamillaDSP



# The CamDSP_config.yaml
You can customize this in a text editor or in the CamillaDSP GUI. There are a few key bits here:
- We have filters named "Filt1", "Filt2", ... "Filt5".  These are ones, by default, configured to be accessible by `camdac.py` and be adjusted with the knobs. You can use different names if you like, but just know that `camdac.py` needs to send configuration updates for the active config that match these names.  Best to set their default gain, initially at least, to zero.
- There's an example "LShelf" filter. You'll have some filters you want always in the pipeline.  Think of these as your "base configuration" if you like and the FiltN as what rides on top of these. Setup whatever you like here in the Filters section and add it to the Pipeline as well.
- We have separate volume filters for L and R to give our balance. They work by using the Aux sliders to reduce gain in one or the other channel
