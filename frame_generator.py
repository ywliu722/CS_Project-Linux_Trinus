import subprocess
import os
import json
from logging import getLogger
from threading import Thread

from drop_queue import DropQueue

log = getLogger(__name__)


class FrameGenerator(Thread):
    width = 1920
    height = 1080

    # size = '640x480'
    framerate = 30
    optirun = False
    vsync = 2

    buffer_size = 1024 * 10

    def __init__(self, settings: dict, buf: DropQueue):
        super(FrameGenerator, self).__init__()
        self.framebuf = buf
        self.settings = settings
        self.end = False

    @property
    def size(self):
        return "%sx%s"%(self.width, self.height)

    @staticmethod
    def api(optirun=False, **kwargs) -> str:
        cmd = "ffmpeg -f x11grab"
        if optirun:
            cmd = "optirun " + cmd
        for i in kwargs.items():
            cmd += " -%s %s" % i
        cmd += " -"
        return cmd

    def run(self):
        params = {
            "loglevel": "error",
            "s": self.size,
            "framerate": self.framerate,
            "i": "{}+0,0".format(os.getenv("DISPLAY")),
            # 'qmin:v': 19,
            "f": "mjpeg",
            "vsync": self.vsync,
        }
        ffmpeg_cmd = self.api(self.optirun, **params)
        command_1 = ffmpeg_cmd
        command_2 = ffmpeg_cmd + "s 1280x720 -"
        log.info("ffmpeg cmd: %s", ffmpeg_cmd)
        p = subprocess.Popen(
            command_1.split(),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )

        data = bytearray()
        start = -1
        quality = ""
        current_quality = "1080p"
        while not self.end:
            try:
                input_file = open ('test.json','r')
                json_array = json.load(input_file)
                input_file.close()
                quality = json_array['quality']
                if quality != current_quality:
                    p.kill()
                    if quality == "1080p":
                        p = subprocess.Popen(
                            command_1.split(),
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                        )
                    elif quality == "720p":
                        p = subprocess.Popen(
                            command_2.split(),
                            shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                        )
                    data = bytearray()
                    start = -1
                    current_quality = quality
            except:
                continue

            data += p.stdout.read(self.buffer_size)

            if start == -1:
                start = data.find(b"\xFF\xD8\xFF")
                continue
            else:
                end = data.find(b"\xFF\xD9")

            if end != -1 and start != -1:
                frame = data[start : end + 1]
                self.framebuf.put(frame)

                data = data[end + 2 :]
                start = -1

        log.info("FrameGenerator end")