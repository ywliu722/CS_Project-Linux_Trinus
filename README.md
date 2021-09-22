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

## Notes (Editted by Yao-Wen Liu)
* If the screen resolution is not 1920x1080, then change the right one in frame_generator.py.
* I only modified frame_generator.py and /callback/mouse.py
    * frame_generator.py
        1. Read test.json and determine which quality to stream.
        2. If the quality is not as the same as current one, then kill the current process, build new one and clear the buffer.
        3. Some functions and variables are not used, e.g. size() and api(), because I just edit the string of command.
        4. Read the document of ffmpeg to get the meaning of the arguments.
    * /callback/mouse.py
        1. The current mouse input is "up-side-down", "opposite left and right" and hold the left button,
            if you want to use this project in 3D-game, you just need to un-comment line 20,21,25,27 and comment line 22,23,26.