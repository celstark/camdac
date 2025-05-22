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