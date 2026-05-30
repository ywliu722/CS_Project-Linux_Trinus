# LinusTrinus (adapted) — Rate-Adaptive Streaming for a Wi-Fi Edge Capstone

> Based on [LinusTrinus](https://github.com/MyrikLD/LinusTrinus) (a TrinusVR
> screen-streaming server for Linux), extended so that streaming quality switches
> on the fly based on Wi-Fi rate-info decisions, with side-by-side output for
> phone-based VR viewing.

## Background

The streaming-server layer of a **solo** undergraduate CS capstone on
*proactive radio-aware adaptation for VR video streaming over a Wi-Fi
edge-computing platform*. It consumes the quality decisions produced by the
[decision module](https://github.com/ywliu722/CS_Project-Pub-Sub), which in turn
reads rate info from the
[mt7915 driver extension](https://github.com/ywliu722/CS_Project-openwrt-mt7915-csi).

The upstream project already streams a captured screen (via FFmpeg) to a TrinusVR
Android client and maps the client's gyroscope motion back to mouse input. My
work was to make that stream **rate-adaptive** and **VR-friendly** for the
capstone.

## What I Changed

The substantive changes are in two files:

- **`frame_generator.py`** — reads the chosen quality from `test.json`; when it
  differs from the current one, kills the running FFmpeg process, starts a new
  one with the new arguments, and clears the buffer, so quality switches live.
  Side-by-side (SBS) output is produced with FFmpeg's
  `-filter_complex [0:v][0:v]hstack`, so a simple phone VR headset (e.g. Google
  Cardboard) gives a near-VR experience without dedicated hardware.
- **`/callback/mouse.py`** — adjusted the gyroscope-to-mouse mapping (orientation
  / drag behavior) for the viewing setup.

Plus minor tweaks: a server-port change in `main.py`, packet-interval timing
instrumentation in `sender.py` (used during measurement), and the `test.json`
quality config.

## Upstream Modes

| Configuration    | Status |
| ---------------- |:------:|
| Mouse            |   OK   |
| SteamVR / OpenVR |   OK   |
| Raw output       |   OK   |

## Dependencies

- Python 3 / PyPy3
- evdev
- FFmpeg
- TrinusVR Android client (Trinus CBVR Lite)

## Running

1. Start the TrinusVR Android client and configure it.
2. Run LinusTrinus: `sudo python3 main.py`
3. Press the start button in the TrinusVR Android client.

## Notes

- If the screen resolution is not 1920x1080, change it in `frame_generator.py`.
- `frame_generator.py` reads `test.json` to pick the streaming quality; when the
  quality changes, it kills the current FFmpeg process, starts a new one, and
  clears the buffer. (Some helpers like `size()` / `api()` are unused — only the
  command string is edited.)
- Output is 3D side-by-side; for regular output, drop the
  `-filter_complex [0:v][0:v]hstack` argument from the FFmpeg command.
- `/callback/mouse.py` is configured for screen viewing (inverted axes + hold to
  drag). For 3D-game use, swap the commented/uncommented lines noted in the file.

## Credits

- Upstream: [MyrikLD/LinusTrinus](https://github.com/MyrikLD/LinusTrinus)
- Original prototype: [ben-romer/LinusTrinus](https://github.com/ben-romer/LinusTrinus)

## Status

Solo undergraduate capstone (2021–22). Working prototype —
[demo video](https://www.youtube.com/watch?v=0c7IfljchAo).
