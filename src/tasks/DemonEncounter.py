import re

from src.tasks.BaseOmjTask import BaseOmjTask
from src.tasks.BaseBattleTask import BaseBattleTask

class DemonEncounter(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-逢魔之时"
        self.description ="暂时未完成测试使用"
        self.default_config.update({
            "DemonEncounter":True,
            "Another_DemonEncounter":False,
            "Monday": "1,1",
            "Tuesday": "1,1",
            "Wednesday": "1,1",
            "Thursday": "1,1",
            "Friday": "1,1",
            "Saturday": "1,1",
            "Sunday": "1,1",
        })
        self.config_description.update({
            "Monday": "每天的队伍",
        })
    def run(self):
        self.in_home_and_back()
        pass
    def DemonEncounter_page(self):
        if not self.wait_click_feature('Home_Town', threshold=0.8, box=self.B('Home_Town'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Town")
        if self.wait_feature('Home', threshold=0.7,
                                        box=self.box_of_screen(0.65, 0.17, 0.91, 0.73),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("Town")
            self.sleep(0.5)
            self.click_relative(0.5, 0.19)
        if self.wait_ocr(match=re.compile("封魔|之时"),time_out=6,
                         box=self.box_of_screen(0.06, 0.01, 0.29, 0.11),):
            self.log_info("封魔之时选择")
            self.sleep(0.5)
            if self.config["DemonEncounter"]:
                self.click_relative(0.83, 0.57)
                if self.wait_ocr(match=re.compile("首领|阴阳|式神"),time_out=6,
                                 box=self.box_of_screen(0.54, 0.87, 0.85, 1.0),):
                    self.log_info("进入封魔之时")
                    self.sleep(0.5)
                    if not self.wait_click_feature('DemonEncounter', threshold=0.8, box=self.box_of_screen(0.54, 0.87, 0.85, 1.0),
                                               raise_if_not_found=False, time_out=6, after_sleep=1):
                        self.log_warning("找不到探索 Home_Town")
                        self.sleep(3)
                        self.click_relative(0.5,0.5)
                        if self.wait_click_ocr(match=re.compile("集结|挑战"),time_out=6,
                                            box=self.box_of_screen(0.7,0.7 , 1, 1.0),):
                            self.log_info("集结挑战")

                        if self.wait_click_ocr(match=re.compile("确定"), time_out=6,
                                            box=self.box_of_screen(0.51,0.53,0.7,0.7),):
                            self.log_info("进入战斗页面")
                            return True
            else:
                return False
            if self.config["Another_Encounter"]:
                self.click_relative(0.42, 0.24)
                self.sleep(0.5)
                if self.wait_ocr(match=re.compile("彼世|封魔"), time_out=6,
                                 box=self.box_of_screen(0.06, 0.01, 0.29, 0.11), ):
                    self.log_info("进入彼时封魔")
                    return True
        return False
    def DemonEncounter_battle(self):
        pass



    