import random
import re

from src.tasks.BuffBattleTask import BuffBattleTask



class HeroTask(BuffBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "战斗-英杰试炼"
        self.description = "暂时只支持阴阳师经验本"
        self.default_config.update({
            "Hero": "源赖光",
        })
        self.config_description.update({
            "Hero":"经验副本选择"
        })
        self.config_type.update({
            "Hero": {
                "type": "drop_down",
                "options": ["源赖光", "藤原道长"],
            },
        })
        self.israikou = True
    def run(self):
        self.in_home_and_back()
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        self.is_sleep, self.count_range, self.time_range = self._random_sleep(self.config["RandomSleep"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        if not self.hero_page():
            return False
        if not self.battle_page():
            return False


    def hero_page(self):
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        self.info_set("步骤", "进入探索页面")

        if self.open_buff(self.config.get("Buff Enable", [])):
            self.log_info("open buff")
        else:
            self.log_info("not open buff")

        if self.wait_click_feature('Exploration_Hero', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击英杰试炼")
        if self.wait_ocr(match=re.compile("英杰|试炼"), box=self.box_of_screen(0, 0, 0.2, 0.2),
                         time_out=6,raise_if_not_found=False):
            self.log_info("进入英杰试炼")
        if res := self.wait_ocr(box=self.box_of_screen(0.02, 0.85, 0.11, 0.97),
                         time_out=6,raise_if_not_found=False):
            text = str(res)
            if "藤原" in text:
                self.israikou = False
            elif "源氏" in text:
                self.israikou = True
            else:
                return False

        if self.config["Hero"] == "源赖光" and not self.israikou:
            self.sleep(1)
            self.click_rect_random((0.04, 0.17, 0.08, 0.23))
            if self.wait_ocr(match=re.compile("选择"), box=self.box_of_screen(0.11, 0, 0.17, 0.1),
                         time_out=6,raise_if_not_found=False):
                self.log_info("进入英杰选择")
            else:
                return False
            self.sleep(1)
            self.click_rect_random((0.2, 0.37, 0.29, 0.54))
            self.israikou = True

        if self.config["Hero"] == "藤原道长" and self.israikou:
            self.sleep(1)
            self.click_rect_random((0.04, 0.17, 0.08, 0.23))
            if self.wait_ocr(match=re.compile("选择"), box=self.box_of_screen(0.11, 0, 0.17, 0.1),
                         time_out=6,raise_if_not_found=False):
                self.log_info("进入英杰选择")
            else:
                return False
            self.sleep(1)
            self.click_rect_random((0.46, 0.38, 0.53, 0.59))
            self.israikou = False
        return True

    def battle_page(self):
        if self.israikou:
            if self.wait_click_ocr(match=re.compile("鬼兵|演武|经验"), box=self.box_of_screen(0.05, 0.39, 0.17, 0.76),
                         time_out=6,raise_if_not_found=False):
                if self.wait_ocr(match=re.compile("鬼兵|演武"), box=self.box_of_screen(0.11, 0, 0.17, 0.1),
                         time_out=6,raise_if_not_found=False):
                    self.log_info("进入鬼兵演武经验副本")
                    self.battle()
                else:
                    return False
        else:
            if self.wait_click_ocr(match=re.compile("传承|试炼|经验"), box=self.box_of_screen(0.22, 0.23, 0.32, 0.68),
                         time_out=6,raise_if_not_found=False):
                if self.wait_ocr(match=re.compile("传承|试炼"), box=self.box_of_screen(0.11, 0, 0.17, 0.1),
                         time_out=6,raise_if_not_found=False):
                    self.log_info("进入传承试炼经验副本")
                    self.battle()
                else:
                    return False
    def battle(self):
        self.count = 1

        if self.is_sleep:
            self.next_sleep_count = random.randrange(*(self.count_range))
        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.56, 0.86, 0.76, 0.99), lock=False)
        else:
            # 不换
            self.Lock_team((0.56, 0.86, 0.76, 0.99), lock=True)
        while self.count <= self.AttackNumber:
            if self.count == 1:
                self.log_info("进入检测1")
                if self.config["Lock Team Enable"]:
                    self.Change_team(self.group, self.team)

                self.log_info("检测是否为自动")
                self.change_auto(self.green, self.GreenNum)
            else:
                self.click_green(self.GreenNum)

            if self.wait_click_ocr(match=re.compile("挑战"), box=self.box_of_screen(0.87, 0.79, 0.97, 0.95),
                                time_out=6,raise_if_not_found=False):
                self.log_info("进入战斗")
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
                self.count += 1
        return True







