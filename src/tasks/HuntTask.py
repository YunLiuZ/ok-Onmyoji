import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class HuntTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-寮内-狩猎战"
        self.description = "暂时不支持换协战的式神，每周的周一到周四"
        self.default_config.update({

        })
        self.config_description.update({

        })
        self.green = {
            1: (0.04, 0.59),
            2: (0.23, 0.43),
            3: (0.37, 0.53),
            4: (0.58, 0.58),
            5: (0.44, 0.92),
            6: (0.2, 0.71),
        }
    def run(self):
        self.in_home_and_back()
        self.is_sleep,self.count_range , self.time_range = self._random_sleep(self.config["RandomSleep"])
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        self.hunt_page()
        if self.battle():
            self.Back_Home()
            return True
        else:return False
    def hunt_page(self):
        if not self.wait_click_feature('YinYang_Lodge', threshold=0.7,
                                        box=self.B('YinYang_Lodge'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到YinYang_Lodge")
        self.info_set("步骤", "进入YinYang_Lodge")
        if self.wait_click_ocr(match=re.compile("狩猎"), time_out=3,
                         box=self.box_of_screen(0.01, 0.21, 0.19, 0.71),
                         raise_if_not_found=False):
            self.log_info("进入狩猎战")
            if self.wait_ocr(match=re.compile("狩猎"), time_out=6,
                             box=self.box_of_screen(0.06, 0.01, 0.24, 0.11),
                             raise_if_not_found=False):
                self.log_info("进入狩猎战")
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
    def battle(self):
        self.sleep(1)
        self.click_rect_random((0.89, 0.8, 0.96, 0.94))
        self.log_info("点击挑战")
        if self.wait_ocr(match=re.compile("预设|加成"),time_out=6,
                         box=self.box_of_screen(0.0, 0.89, 0.14, 1),
                         raise_if_not_found=False):
            self.log_info("进入狩猎战战斗页面")
        if self.config["Lock Team Enable"]:
            self.Change_team(self.group, self.team)
        self.sleep(1)
        self.log_info("点击准备")
        self.click_rect_random((0.87, 0.73, 0.96, 0.86))
        self.log_info("检测是否为自动")
        self.change_auto(self.green,self.GreenNum)
        if self.wait_click_feature('Battle_Success', threshold=0.8,
                                box=self.box_of_screen(0.2, 0, 0.5, 0.43),
                                raise_if_not_found=False,
                                time_out=self.BattleTime,
                                after_sleep=0.5):
            self.log_info("战斗完成")
            return True
        else:
            self.log_info("战斗失败")
            return False

