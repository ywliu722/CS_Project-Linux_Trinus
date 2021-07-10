# LinusTrinus

TrinusVR screen streaming server for Linux

## Modes
|      Configuration      |   Status  |
| ----------------------- |:---------:|
| Mouse                   |   OK      |
| SteamVR / OpenVR        |   OK      |
| Raw output              |   OK      |


## Dependencies

* Python3 / Pypy3
* evdev
* ffmpeg
* TrinusVR android client

## Running

1. Start the TrinusVR Android client and configure it.
2. Run LinuxTrinus: `sudo python3 main.py`
3. Press the start button in the TrinusVR Android client.

## Reference and source code

* [ben-romer](https://github.com/ben-romer/LinusTrinus) - Prototype

## Notes

* Because I only use mouse, so I put the OpenVR related file in a directory.
* If the screen resolution is not 1920x1080, then change the right one in frame_generator.py.