import re
import random
from datetime import datetime, timedelta
from src.tasks.BaseBattleTask import BaseBattleTask
from datetime import datetime, timedelta
from src.tasks.BuffBattleTask import BuffBattleTask

class GoryouRealmTask(BuffBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "战斗-御灵"
        self.default_config.update({
            "GoryouRealm": "神龙",
        })
        self.config_description.update({
        })
        self.config_type.update({
            "GoryouRealm": {
                "type": "drop_down",
                "options": ["神龙", "白藏主", "黑豹","孔雀"],
            },
        })
    def run(self):
        self.in_home_and_back()
        self.count = 1
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        if not self.GoryouRealm_page():
            self.log_warning("找不到页面")
            return False
        if not self.battle():
            self.log_warning("Leader_page 失败")
            return False
        self.Back_Home()

    def GoryouRealm_page(self):
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        if self.config["Buff Enable"] and self.count == 1:
            if self.open_buff(self.config.get("Buff Enable", [])):
                self.log_info("open buff")
            else:
                self.log_info("not open buff")
        if self.wait_click_feature('Exploration_GoryouRealm', threshold=0.7,
                                   box=self.B('bottom'),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击御灵")
        if text := self.wait_ocr(match=re.compile("御灵|之境"), box=self.box_of_screen(0.11, 0, 0.17, 0.1)):
            self.log_info("进入御灵页面")
            self.sleep(1)
            if self.config["GoryouRealm"] == "神龙":
                self.click_rect_random((0.11, 0.22, 0.22, 0.53))
            elif self.config["GoryouRealm"] == "白藏主":
                self.click_rect_random((0.36, 0.21, 0.47, 0.52))
            elif self.config["GoryouRealm"] == "黑豹":
                self.click_rect_random((0.58, 0.22, 0.71, 0.54))
            else:
                self.click_rect_random((0.82, 0.22, 0.95, 0.54))
            return True
        return False
    def battle(self):
        self.count = 1
        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.53, 0.9, 0.63, 1.0), lock=False)
        else:
            # 不换
            self.Lock_team((0.53, 0.9, 0.63, 1.0), lock=True)
        while self.count <= self.AttackNumber:
            if self.wait_click_ocr(match=re.compile("挑战"), box=self.box_of_screen(0.79, 0.75, 0.93, 0.98),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
                self.log_info("进入战斗")
            if self.count == 1:
                self.log_info("进入检测1")
                if self.config["Lock Team Enable"]:
                    self.Change_team(self.group, self.team)

                self.log_info("检测是否为自动")
                self.change_auto(self.green, self.GreenNum)
            else:
                self.click_green(self.GreenNum)
            res = self.Find_finish(self.BattleTime)
            if res == 2:
                self.log_warning("战斗失败！！")
                return False
            elif res == 3:
                self.log_warning("战斗超时！！")
                return False

            if self.is_sleep:
                self.log_info(f"会在第{self.next_sleep_count}次休息")
                if self.count >= self.next_sleep_count:
                    self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                    a = random.randrange(*(self.time_range))
                    self.log_info(
                        f"第 {self.count} 次战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                    self.sleep(a)
            else:
                self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber}")
            self.count += 1
            self.trigger_count += 1
        return True
