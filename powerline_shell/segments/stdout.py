import subprocess
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        cmd = self.segment_def["command"]
        self.output = subprocess.check_output(cmd).decode("utf-8").strip()

    def add_to_powerline(self):
        self.join()
        fg_color = self.segment_def.get("fg_color", self.powerline.theme.PATH_FG)
        bg_color = self.segment_def.get("bg_color", self.powerline.theme.PATH_BG)
        self.powerline.append(" %s " % self.output, fg_color, bg_color) 
