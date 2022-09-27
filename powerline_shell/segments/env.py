import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
		var_value = os.getenv(self.segment_def["var"])
		if (not var_value and
			self.segment_def.get("skip_undefined", False)):
			return
		self.powerline.append(
            " %s " % var_value,
            self.segment_def.get("fg_color", self.powerline.theme.PATH_FG),
            self.segment_def.get("bg_color", self.powerline.theme.PATH_BG))