# Setting up the raspberry pi for gaming

## Power-on the pi

Be sure that the pi is set-up (with OS connected) before plugging-in (plugging in turns it on).
Note:  We DO have a power-switch for the pi.

## Update the pi

```
sudo apt update
sudo apt upgrade
```

Note: If you need the password, the default username is "pi" and the default password is "raspberry".

## Check the version of python
We should have at least python 3--this should default to python 3.5 at the earliest (anything earlier and we should check for compatibility issues or upgrade python).

```
python3 --version
```

## Install arcade on python3

Note: "pip" will install to an earlier version of python, so be sure to use pip3 in case the pi has Python 2.7 installed standard (many things do, and at least one of our pis does).

```
pip3 install arcade
```

## (Posisbly) Install numpy.

Numpy is likely already standard on python, but just in case, you made need to install that module.
This isn't a bad idea anyway, because it'll give you a version that may be more up to date.

```
pip3 install numpy
```

## Load "qg_game_5" folder over from flash drive

This folder contains all of the sounds, images, simulation code, etc for the game.


## Give execution-access to "playground_for_testing.py"

```
chmod +x playground_for_testing.py
```

Until the newest/latest version of the game is added, this is the file to run (likely to change filenames once complete)
