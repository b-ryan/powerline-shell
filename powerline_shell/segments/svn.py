import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        is_svn = subprocess.Popen(["svn", "status"],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        is_svn_output = is_svn.communicate()[1].decode("utf-8").strip()
        if len(is_svn_output) != 0:
            return
        p1 = subprocess.Popen(["svn", "status"], stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "-c", r"^[ACDIMR\!\~]"],
                stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()[0].decode("utf-8").strip()
        if len(output) > 0 and int(output) > 0:
            changes = output.strip()
            powerline.append(" %s " % changes,
                             powerline.theme.SVN_CHANGES_FG,
                             powerline.theme.SVN_CHANGES_BG)
