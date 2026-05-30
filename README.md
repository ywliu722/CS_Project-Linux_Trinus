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

## Tech Stack

- **Language:** Python 3 / PyPy3
- **Capture / encode:** FFmpeg
- **Input injection:** python-evdev
- **Client:** TrinusVR Android client (Trinus CBVR Lite)

## Credits

- Upstream: [MyrikLD/LinusTrinus](https://github.com/MyrikLD/LinusTrinus)
- Original prototype: [ben-romer/LinusTrinus](https://github.com/ben-romer/LinusTrinus)

## Status

Solo undergraduate capstone (2021–22). Working prototype —
[demo video](https://www.youtube.com/watch?v=0c7IfljchAo).
