import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class DuelTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "周常-斗技"
        self.description = "名仕以下挂机,如果长时间没有玩过斗技，请先手动进入一次，消除弹窗"
        self.rank = 0 #斗技分数
        self.rank_num = 0 #斗技段数
        self.default_config.update({
            "Duel":"名仕"
        })
        self.config_type.update({
            "Duel": {
                "type": "drop_down",
                "options": ["一段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "名仕"],
            },
        })
        self.config_description.update({
            "Duel":"挂到什么段停止挂机"
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
        # self.is_sleep,self.count_range , self.time_range = self._random_sleep(self.config["RandomSleep"])
        # self.group, self.team = self._parse_preset(self.config["Preset Team"])
        # if self.config["Preset Enable"]:
        #     self.SwitchSoul_by_num(self.group, self.team)

        self.duel_page()
    def duel_page(self):
        if not self.wait_click_feature('Home_Town', threshold=0.8,
                                          time_out=6, box=self.B('Home_Town'),
                                          raise_if_not_found=False):
            self.log_warning("没有进入町中")
        if self.wait_click_feature('Duel', threshold=0.8,
                                          time_out=6, box=self.box_of_screen(0.57, 0.16, 0.65, 0.34),
                                          raise_if_not_found=False):
            self.log_warning("进入斗技")
            self.sleep(1)
        else:
            self.log_warning("没找到斗技如楼")
            return False
        self.click_rect_random((0.3, 0.05, 0.7, 0.18))#长时间不进入消除弹窗
    def battle(self):
        res = self.wait_ocr(match=re.compile("一段|二段|三段|四段|五段|六段|七段|八段|九段"),
                             time_out=3,
                             box=self.box_of_screen(0.44, 0.55, 0.58, 0.68),
                             raise_if_not_found=False, )
        self.log_info(f"当前的段位为{res}")
        self.count = 1
        while self.count <= self.AttackNumber:
            if self.wait_ocr(match=re.compile("斗技"),
                                    time_out=3,
                                    box=self.box_of_screen(0, 0, 0.2, 0.2),
                                    raise_if_not_found=False, ):
                self.log_info(f"进入战斗准备页面")
            if res:=self.wait_ocr(match=re.compile("一段|二段|三段|四段|五段|六段|七段|八段|九段"),
                             time_out=3,
                             box=self.box_of_screen(0.44, 0.55, 0.58, 0.68),
                             raise_if_not_found=False,):
                self.log_info(f"当前的段位为{res}")
            self.sleep(1)
            self.click_rect_random((0.9, 0.79, 0.97, 0.9)) #start




