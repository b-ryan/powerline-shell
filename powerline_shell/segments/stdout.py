import subprocess
from ..utils import ThreadedSegment, warn


class Segment(ThreadedSegment):
    def run(self):
        cmd = self.segment_def.get("command", [])

        if len(cmd) == 0:
            warn("no command specified")
            self.output = None
            return

        try:
            self.output = subprocess.check_output(cmd).decode("utf-8").strip()
            self.success = True
        except subprocess.CalledProcessError as ex:
            if self.segment_def.get("allow_error", True):
                self.output = ex.output.decode("utf-8").strip()
            else:
                self.output = None

            self.success = False

        # TODO handle malformed command

    def add_to_powerline(self):
        self.join()

        if self.output is None:
            return

        if self.success:
            fg_color = self.segment_def.get("fg_color", self.powerline.theme.PATH_FG)
            bg_color = self.segment_def.get("bg_color", self.powerline.theme.PATH_BG)
        else:
            fg_color = self.segment_def.get("error_fg_color", self.powerline.theme.CMD_FAILED_FG)
            bg_color = self.segment_def.get("error_bg_color", self.powerline.theme.CMD_FAILED_BG)

        for i, line in enumerate(self.output.split("\n")):
            line = line.strip()
            if len(line) == 0 and self.segment_def.get("hide_empty", False):
                continue

            if i > 0:
                self.powerline.append("\n",
                    self.powerline.theme.RESET,
                    self.powerline.theme.RESET,
                    separator="")
            self.powerline.append(" %s " % line, fg_color, bg_color)
