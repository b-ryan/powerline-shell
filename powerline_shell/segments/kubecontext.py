"""
Shows the exported kubectl context
e.g $ export KUBECONFIG=~/.kube/config-staging-cluster
"""
from ..utils import BasicSegment
import os


class Segment(BasicSegment):
    def add_to_powerline(self):
        kubecontext = os.environ.get("KUBECONFIG")
        if kubecontext:
            self.powerline.append(" kctx:%s " % os.path.basename(kubecontext),
                                  self.powerline.theme.KUBECONFIG_FG,
                                  self.powerline.theme.KUBECONFIG_BG)
