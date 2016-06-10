# Jumper : a python game

Jumper is a small platform-game written in python with the pygame library.

## Install

### Linux

You must install pygame for python 3 :

Install the dependencies :
> sudo apt-get install python3-dev python3-numpy libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libsdl1.2-dev  libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libfreetype6-dev

Install mercurial to clone pygame's sources
> sudo apt-get install mercurial

And clone
> hg clone https://bitbucket.org/pygame/pygame

Then  go to the directory, buitld and install pygame
> cd pygame

> python3 setup.py build

> sudo python3 setup.py install

And install python3-yaml :

> sudo apt-get install python3-yaml

### Windows

Download and install python3.4. You can find the installer at the bottom of this page : https://www.python.org/downloads/release/python-343/


Download pygame (pick "pygame-1.9.2a0-cp34-none-win32.whl" or "pygame-1.9.2a0-cp34-none-win32\_amd64.whl" : http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame) and place it into C:\\Python34\\Scripts\\[pygame-1.9.2a0-cp34-none-win32.whl/pygame-1.9.2a0-cp34-none-win32\_amd64.whl]

Open a cmd into C:\\Python34\\Scripts\\ and type 

> pip install [pygame-1.9.2a0-cp34-none-win32.whl/pygame-1.9.2a0-cp34-none-win32\_amd64.whl]

And install PyYAML (pick "PyYAML-3.11.win-amd64-py3.4.exe" or "PyYAML-3.11.win32-py3.4.exe" : http://pyyaml.org/wiki/PyYAML)

To run the game, double click on jumper.py

