
# Case to improve
- You need to remove the SD card to get the board in and out.  1 mm more and we'd clear
- Different knobs, 4 controls, or a bit bigger case -- it's a bit cramped

# Software to-do
- Getting clicks between tracks at least with Shairplay
- Handle offset / pre-amp gain
- Run `camdac.py` as a service
- Add ability to re-define filters more easily

# Hardware to-do
- USB "gadget" mode for inline digital PEQ

-----------
Desktop audio not working -- https://github.com/HEnquist/camilladsp-config
- Put their asound.conf into /etc/
- 


# Gadget mode

- Figure your current DAC's capable modes. If it's plugged into a Linux box `aplay -l` to list the devices. In my case, the Fulla was on card1.  Then, see what modes are supported `cat /proc/asound/card1/stream0`.  So, all typical suspects from 44100 - 384000, 16_LE, 24_3LE, and 32_LE

- Set the RPi up to run in gadget mode and offer up an audio interface. Instructions are ocming from [mdsimon2](https://github.com/mdsimon2/RPi-Camilla). It's also good to have [DeLub's post on ASR](https://www.audiosciencereview.com/forum/index.php?threads/using-a-raspberry-pi-as-equaliser-in-between-an-usb-source-ipad-and-usb-dac.25414/page-3#post-1180356) on hand (we're well past the need to compile anything in that thread though). For now, I'm just going to offer up 44100 like mdsimon2 did 
```
echo 'dtoverlay=dwc2' | sudo tee -a /boot/firmware/config.txt > /dev/null
echo -e 'dwc2\ng_audio' | sudo tee -a /etc/modules > /dev/null
echo 'options g_audio c_srate=44100 c_ssize=4 c_chmask=3 p_chmask=0' | sudo tee -a /etc/modprobe.d/usb_g_audio.conf > /dev/null 

sudo reboot now
```
- Use the USB-C power/data splitter. Power supply goes into power (duh), USB2 data goes to your computer, USB/data goes to Rpi.  On the RPi then, have a USB2 port go to your DAC.  You should get your USB chime.  If you're on a Linux host, you should see a "Linux USB Audio Gadget" with `aplay -l` or `lsusb`. You should see the audio format available as well with `cat /proc/asound/card1/stream0` (change card1 to yoru card number from aplay or lsusb) 
- On the RPi, we need to setup CamillaDSP to now be able to listen to this input, do its DSP, and then send out.
  - Run `aplay -L` and look for your DAC. It'll give a big list of possible devices. I've been having Camilla output to `hw:CARD=DAC` to send audio to my RPi DAC.  Look for an "hw" one that shows your device.  Mine is `hw:CARD=Schiit`. It may help to run `aplay -L | grep hw` to filt out and just get the "hw" ones.
  - In that `aplay -L` you should see `usbstream:CARD=UAC2Gadget` (or possibly hw:UAC2Gadget`)
  - In the CamillaDSP GUI, head to Files, enter in "gadget" or some such name at the bottom of the Configs panel, hit Save and star it to mark as active.  
  - In its Devices, set: samplerate=44100 (if you're resampling, you should be able to keep that at your 88200 or whatever you like too), capture device / device = "hw:CARD=UAC2Gadget" (even if it showed as _usbstream_), and Playback device / device = "hw:NAME".  In my case, it was `hw:Schiit` (you can also use `hw:CARD=Schiit`)


Another great project by [Wang-Yue](https://github.com/Wang-Yue/CamillaDSP-Gadget)