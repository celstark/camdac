# Install CamillaDSP

Following [mdsimon2's instructions](https://github.com/mdsimon2/RPi-CamillaDSP)
```
mkdir ~/camilladsp ~/camilladsp/coeffs ~/camilladsp/configs
wget https://github.com/HEnquist/camilladsp/releases/download/v3.0.1/camilladsp-linux-aarch64.tar.gz -O ~/camilladsp/camilladsp-linux-aarch64.tar.gz
sudo tar -xvf ~/camilladsp/camilladsp-linux-aarch64.tar.gz -C /usr/local/bin/

sudo wget https://raw.githubusercontent.com/mdsimon2/RPi-CamillaDSP/main/camilladsp.service -O /lib/systemd/system/camilladsp.service

...

```

Since using the DAC board, make sure to turn off the onboard sound by commenting out the audio with `#dtparam=audio=on` in `/boot/firmware/config.txt`
```

# Install pyCamillaDSP
This *really* wants me in an venv or conda env, so for now, such is life... Make sure though to include the system packages or you'll miss out on all the RPi bits
```
python -m venv  --system-site-packages ~/camilladsp/.venv
source ~/camilladsp/.venv/bin/activate
pip install git+https://github.com/HEnquist/pycamilladsp.git

```

Either activate it each time or `~/camilladsp/.venv/bin/python some_script.py` to run code.


# Testing
sudo service shairport-sync restart
speaker-test -D hw:Loopback,1 -c 2 -r 44100 -F S32_LE



# Case
The case came from [Pieterbos82](https://www.thingiverse.com/thing:4753525) on Thingiverse originally.  I took his SCAD code, fumbled my way through SCAD, and revised it.  Notably, I turned off the Neutrik / XLR bits, reworked the DAC HAT spacing for the IQAudio / RaspberyPi branded DAC boards, and added holes in the "front" for our controls.

## To improve
- You need to remove the SD card to get the board in and out.  1 mm more and we'd clear
- Different knobs, 4 controls, or a bit bigger case -- it's a bit cramped
