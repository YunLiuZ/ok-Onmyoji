import re

from src.tasks.BaseBattleTask import BaseBattleTask
from datetime import datetime, timedelta
class SecretTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "周常-秘闻竞速"

        self.default_config.update({
        })
        self.config_description.update({
        })
    def run(self):
        self.in_home_and_back()
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        if not self.secret_page():
            self.log_warning("找不到页面")
            return False
        if not self.secret_battle():
            self.log_warning("秘闻失败")
            return False
    def secret_page(self):
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        self.info_set("步骤", "进入探索页面")

        if self.wait_click_feature('Exploration_Secret', threshold=0.7,
                                   box=self.B('bottom'),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("探索 Exploration_Secret")
        if self.wait_ocr(match=re.compile("秘闻|副本"),
                                   time_out=6,
                                   box=self.box_of_screen(0, 0, 0.17, 0.1)):
            self.log_info("进入秘闻页面")
            self.click_relative(0.5,0.1)
            self._swipe(0.36, 0.22, 0.37, 0.86, 0.2)
            self._swipe(0.36, 0.22, 0.37, 0.86, 0.2)
            self._swipe(0.36, 0.3,0.37, 0.81,0.2)
            self.sleep(1)
            self.click_relative(0.22, 0.24)
            if self.wait_click_ocr(match=re.compile("进入"),
                                box=self.box_of_screen(0.88, 0.82, 0.97, 0.95),
                                raise_if_not_found=False,
                                time_out=3,):
                self.log_info("进入竞速")
            return True
        else:
            self.log_info('找不到秘闻')
            return False
    def secret_battle(self):
        if self.wait_ocr(match=re.compile("未通关|未解锁|壹|贰|叁|肆|伍|陆|柒|捌|玖|拾"),
                               box=self.box_of_screen(0.16, 0.21, 0.45, 0.9),
                               time_out=3,
                               raise_if_not_found=False):
            self.log_info("进入秘闻战斗")
        self.count = 1
        if self.config["Lock Team Enable"]:
            self.log_info("1")
            #解锁状态 准备换队伍
            self.Lock_team((0.86, 0.93, 0.9, 1.0),lock=False)
        else:
            #不换
            self.Lock_team((0.86, 0.93, 0.9, 1.0), lock=True)
        while self.count <= 10 and self.wait_click_ocr(match=re.compile("未通关"),
                               box=self.box_of_screen(0.33, 0.21, 0.43, 0.89),
                               time_out=3,
                               raise_if_not_found=False) :
            self.count <= 10 and self.wait_click_ocr(match=re.compile("未通关"),
                                                     box=self.box_of_screen(0.33, 0.21, 0.43, 0.89),
                                                     time_out=3,
                                                     raise_if_not_found=False)
            if self.trigger_count >= 2:
                self.log_info("进入第二次战斗锁住阵容")
                self.Lock_team((0.50, 0.70, 0.70, 0.90), lock=True)
            self.click_relative(0.9,0.82)
            self.log_info("进入战斗")

            if self.count == 1:
                self.log_info("进入检测1")
                if self.config["Lock Team Enable"]:
                    self.Change_team(self.group, self.team)

                self.log_info("检测是否为自动")
                self.change_auto(self.GreenNum)
            else:
                self.click_green(self.GreenNum)

            res = self.secret_battle_find_finish()
            if res == 2:
                self.log_warning("战斗失败！！")
                return False
            elif res == 3:
                self.log_warning("战斗超时！！")
                return False
            self.log_info(f"第 {self.count} 个挑战")
            self.count += 1
        self.sleep(1)
        self.click_relative(0,0.06)
        if self.Back_Home():
            return True
        else:
            return False
    def secret_battle_find_finish(self):
        """
                等待战斗结束并处理结算画面。

                Returns:
                    1  战斗成功
                    2  战斗失败
                    3  超时
                """
        result = 1
        def check():
            nonlocal result
            if self.wait_click_feature('Battle_Finish', threshold=0.7,
                                       box=self.B('Battle_Finish'),
                                       raise_if_not_found=False, time_out=1,
                                       after_sleep=0.5):
                if res1 := self.find_one('Battle_Finish', threshold=0.7,
                                         box=self.B('Battle_Finish')):
                    self.click(res1)
                    self.sleep(0.5)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            if self.ocr(match=re.compile("提升|再次|阴阳师"),
                                box=self.box_of_screen(0.22, 0.53, 0.79, 0.8)):
                result = 2
                return True
            else:
                return False

        if self.wait_until(check, time_out=self.BattleTime, raise_if_not_found=False):
            return result

        self.log_warning("战斗结束超时")
        return 3




