import subprocess
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def add_to_powerline(self):
        p1 = subprocess.Popen(["kubectl", "config", "current-context"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        k8s_context = p1.communicate()[0].decode("utf-8").rstrip()
        if not k8s_context:
            return
        self.powerline.append(" " + k8s_context + " ", self.powerline.theme.K8S_CONTEXT_FG, self.powerline.theme.K8S_CONTEXT_BG)
