from ..utils import BasicSegment
import subprocess

class Segment(BasicSegment):
    def add_to_powerline(self):
        try:
            kube_env = subprocess.check_output(['kubectl', 'config', 'current-context'], stderr=subprocess.STDOUT)
            if 'not set' in kube_env:
                raise Exception('k8s: Not set')
        except:
            kube_env = None

        if kube_env:
            self.powerline.append(" %s " % str.strip(kube_env),
                                  self.powerline.theme.KUBECONFIG_PATH_FG,
                                  self.powerline.theme.KUBECONFIG_PATH_BG)
