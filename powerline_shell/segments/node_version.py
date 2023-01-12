import subprocess
from ..utils import ThreadedSegment, find_upwards


class Segment(ThreadedSegment):
    def run(self):
        try:
            p1 = subprocess.Popen(["node", "--version"], stdout=subprocess.PIPE)
            self.version = p1.communicate()[0].decode("utf-8").rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()

        require_package = self.powerline.segment_conf("node_version", "require_package", False)
        chars = int(self.powerline.segment_conf("node_version", "chars", 10))
        has_package = find_upwards("package.json") != None

        if require_package and not has_package:
            return
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append(" node " + self.version[:chars] + " ", 15, 18)
