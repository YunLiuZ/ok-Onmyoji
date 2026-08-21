import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class GateTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-寮内-阴界之门"
        self.description = "暂未完成，先挖坑"
        self.default_config.update({

        })
        self.config_description.update({

        })
    def run(self):
        pass
    def gate_page(self):
        if not self.wait_click_feature('YinYang_Lodge', threshold=0.7,
                                        box=self.B('YinYang_Lodge'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到YinYang_Lodge")
        self.info_set("步骤", "进入YinYang_Lodge")
        if self.wait_click_ocr(match=re.compile("阴界|之门"), time_out=3,
                         box=self.box_of_screen(0.01, 0.21, 0.19, 0.71),
                         raise_if_not_found=False):
            self.log_info("进入阴界之门")
            if self.wait_ocr(match=re.compile("阴界|之门"), time_out=6,
                             box=self.box_of_screen(0.06, 0.01, 0.24, 0.11),
                             raise_if_not_found=False):
                self.log_info("进入阴界之门")
                return True
            else:
                return False
        if not self.wait_click_feature("YinYang_Shrine", threshold=0.7,
                                        box=self.box_of_screen(0.65, 0.83, 0.76, 0.99),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到YinYang_Shrine")
        if not self.wait_click_feature("YinYang_Hunt", threshold=0.7,
                                       box=self.box_of_screen(0.08, 0.49, 0.31, 0.87),
                                       raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到YinYang_Hunt")
        if self.wait_ocr(match=re.compile("狩猎"),time_out=6,
                         box=self.box_of_screen(0.06, 0.01, 0.24, 0.11),
                         raise_if_not_found=False):
            self.log_info("进入狩猎战")
            return True
        else:
            self.log_warning("没有进入狩猎")
            return False