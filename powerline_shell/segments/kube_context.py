"""
Shows the exported kubectl context
e.g $ export KUBECONFIG=~/.kube/config-staging-cluster
"""
from ..utils import BasicSegment
import os


class Segment(BasicSegment):
    def add_to_powerline(self):
        kube_context = os.environ.get("KUBECONFIG")
        if kube_context:
            self.powerline.append(" kctx:%s " % os.path.basename(kube_context),
                                  self.powerline.theme.KUBE_CONTEXT_FG,
                                  self.powerline.theme.KUBE_CONTEXT_BG)

