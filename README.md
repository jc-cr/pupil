# Fork of Pupil Core

Installation 
```sh
git clone https://github.com/jc-cr/pupil.git
cd pupil
git checkout develop
python -m pip install -r requirements.txt
```
#### Linux

##### USB Access

To grant Pupil Core applications access to the cameras, run

```sh
echo 'SUBSYSTEM=="usb",  ENV{DEVTYPE}=="usb_device", GROUP="plugdev", MODE="0664"' | sudo tee /etc/udev/rules.d/10-libuvc.rules > /dev/null
sudo udevadm trigger
```

and ensure that your user is part of the `plugdev` group:

```sh
sudo usermod -a -G plugdev $USER
```

##### Audio Playback

The [`sounddevice`](https://python-sounddevice.readthedocs.io/en/0.4.5/installation.html#installation) package depends on the `libportaudio2` library:

```sh
sudo apt install libportaudio2
```

### Run Pupil

```sh
cd pupil_src
python main.py capture # or player/service
```

#### Command Line Arguments

The following arguments are supported:

| Flag                   | Description                              |
| ---------------------- | ---------------------------------------- |
| `-h, --help`           | Show help message and exit.              |
| `--version`            | Show version and exit.                   |
| `--debug`              | Display debug log messages.              |
| `--profile`            | Profile the app's CPU time.              |
| `-P PORT, --port PORT` | (Capture/Service) Port for Pupil Remote. |
| `--hide-ui`            | (Capture/Service) Hide UI on startup.    |
| `<recording>`          | (Player) Path to recording.              |



## License
All source code written by Pupil Labs is open for use in compliance with the [GNU Lesser General Public License (LGPL v3.0)](http://www.gnu.org/licenses/lgpl-3.0.en.html). We want you to change and improve the code -- make a fork! Make sure to share your work with the community!
