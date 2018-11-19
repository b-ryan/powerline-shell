import subprocess
from ..utils import RepoStats, ThreadedSegment, get_git_subprocess_env, warn


def get_vcs_dir():
    git_return_code = subprocess.Popen("git status", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    git_return_code.communicate()[0].strip()   # Blocks until 'git status' completes execution
    hg_return_code = subprocess.Popen("hg status", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    hg_return_code.communicate()[0].strip()   # Blocks until 'git status' completes execution
    svn_return_code = subprocess.Popen("svn status", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    svn_stdout = svn_return_code.communicate()[0].strip()   # Blocks until 'git status' completes execution
    if "warning: W155007" not in str(svn_stdout):
        svn_true = False
    else:
        svn_true = True
    if git_return_code.returncode==0 or hg_return_code.returncode==0 or svn_true is False:
        return True
    else:
        return False


class Segment(ThreadedSegment):
    def run(self):
        self.in_vcs_dir = get_vcs_dir()

    def add_to_powerline(self):
        self.join()
        if not self.in_vcs_dir:
            return
        if self.powerline.args.shell == "tcsh":
            warn("newline segment not supported for tcsh (yet?)")
            return
        self.powerline.append("\n",
                                self.powerline.theme.RESET,
                                self.powerline.theme.RESET,
                                separator="")

