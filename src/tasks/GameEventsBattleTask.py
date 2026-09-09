import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask

from datetime import datetime

class GameEventsBattleTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "活动-战斗-当期爬塔"
        self.description = "2026.9.9周年庆爬塔,建议每日手动领取活动票，消除弹窗"
        self.count = 0


        self.isap = True

        self.ap_tickets = 0
        self.general_tickets = 0

        self.default_config.update({
            "ApMode": True,
            "GeneralClimb": True,
            "IsOcr":True,
            "GeneralTickets": "0",
            "ApTickets": "0"
        })
        self.config_description.update({
            "IsOcr": "是否采用自动识别票数，当识别不出请关闭该参数然后手动填写",
            "GeneralTickets": "普通票数量",
            "ApTickets": "体力票数量",
            "AttackNumber": "无需填写",


        })

    def run(self):
        self.in_home_and_back()
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        self.is_sleep, self.count_range, self.time_range = self._random_sleep(self.config["RandomSleep"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        self.Battle_page()
        self.Battle()

    def Battle_page(self):
        self.click_rect_random((0.35, 0.33, 0.38, 0.37))
        self.sleep(3)
        if self.wait_ocr(match=re.compile("战斗|回响|日地"),
                             time_out=3,
                             box=self.box_of_screen(0.2, 0.15, 0.37, 0.48),
                             raise_if_not_found=False):
            self.log_info("进入战斗页面")
            self.sleep(1)
            self.click_rect_random((0.25, 0.27, 0.29, 0.37))
            self.sleep(3)
            if self.wait_click_ocr(match=re.compile("虚无|精锐|战斗"),
                                 time_out=3,
                                 box=self.box_of_screen(0.01, 0.12, 0.23, 0.24),
                                 raise_if_not_found=False):
                self.log_info("进入战斗")
                self.sleep(1)
                return True
        elif self.wait_feature('Event_Finish_2', threshold=0.7,
                                    box=self.box_of_screen(0.34, 0.22, 0.65, 0.44),
                                        raise_if_not_found=False,
                                        time_out=3):
            self.sleep(0.5)
            self.click_rect_random((0.89, 0.24, 0.92, 0.29))
            self.sleep(1)
            self.click_rect_random((0.7, 0.86, 0.73, 0.93))
            self.sleep(1)
            self.click_rect_random((0.89, 0.24, 0.92, 0.29))
            self.sleep(1)
            self.click_rect_random((0.89, 0.24, 0.92, 0.29))
            if self.wait_ocr(match=re.compile("战斗|回响|日地"),
                             time_out=3,
                             box=self.box_of_screen(0.2, 0.15, 0.37, 0.48),
                             raise_if_not_found=False):
                self.log_info("进入战斗页面")
                self.sleep(1)
                self.click_rect_random((0.25, 0.27, 0.29, 0.37))
                self.sleep(3)
                if self.wait_click_ocr(match=re.compile("虚无|精锐|战斗"),
                                       time_out=3,
                                       box=self.box_of_screen(0.01, 0.12, 0.23, 0.24),
                                       raise_if_not_found=False):
                    self.log_info("进入战斗")
                    self.sleep(1)
                    return True
        else:
            self.log_warning("没有进入战斗页面")
            return False

    def Battle(self):
        if self.wait_ocr(match=re.compile("虚无|精锐"),
                         time_out=3,
                         box=self.box_of_screen(0,0,0.3,0.15)):
            self.sleep(3)
            if self.ocr(match=re.compile("御魂|自选"),
                             box=self.box_of_screen(0.0, 0.60, 0.21, 0.70)):
                self.log_info("现在是普通模式")
                self.isap = False
            else:
                self.log_info("现在是体力模式")
                self.isap = True
        else:
            self.log_warning("没有进入战斗页面")
            return False
        if not self.config["IsOcr"]:
            self.ap_tickets = int(self.config["ApTickets"])
            self.general_tickets = int(self.config["GeneralTickets"])
            self.log_info(f"体力爬塔票数{self.ap_tickets}")
            self.log_info(f"普通爬塔票数：{self.general_tickets}")
        else:
            if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.58, 0.0, 0.66, 0.1)):
                nums = re.findall(r'\d+', text[0].name)
                self.general_tickets = int(nums[0]) if nums else 0
                self.log_info(f"普通爬塔票数：{self.general_tickets}")

            if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.42, 0.0, 0.54, 0.1)):
                nums = re.findall(r'\d+', text[0].name)
                self.ap_tickets = int(nums[0]) if nums else 0
                self.log_info(f"体力爬塔票数{self.ap_tickets}")

        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.66, 0.88, 0.72, 0.99), lock=False)
        else:
            # 不换
            self.Lock_team((0.66, 0.88, 0.72, 0.99), lock=True)


        if self.config["GeneralClimb"]:
            self.count = 0
            self.log_info(self.count_range)
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
                self.log_info(f"下次休息{self.next_sleep_count}")
            if self.isap:
                self.click_rect_random((0.96, 0.76, 0.98, 0.79))
                self.log_info("切换为普通爬塔")
                self.isap = False
                self.sleep(0.5)
            else:
                self.log_info("普通爬塔")
            while self.count < self.general_tickets:
                self.Battle_process()
                self.count += 1
                if self.is_sleep:
                    self.log_info(f"会在第{self.next_sleep_count}次休息")
                    if self.count >= self.next_sleep_count:
                        self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                        a = random.randrange(*(self.time_range))
                        self.log_info(f"第 {self.count} 次普通爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                        self.sleep(a)
                self.log_info(f"第 {self.count} 次普通爬塔战斗结束 总共{self.general_tickets}，下次休息{self.next_sleep_count}")

        if self.config["ApMode"]:
            self.count=0
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
            if not self.isap:
                self.click_rect_random((0.96, 0.76, 0.98, 0.79))
                self.log_info("切换为刷体力")
                self.isap = True
                self.sleep(0.5)
            else:
                self.log_info("体力")
            while self.count < self.ap_tickets:
                self.Battle_process()
                self.count += 1
                if self.is_sleep:
                    self.log_info(f"会在第{self.next_sleep_count}次休息")
                    if self.count >= self.next_sleep_count:
                        self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                        a = random.randrange(*(self.time_range))
                        self.log_info(f"第 {self.count} 次体力爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                        self.sleep(a)
                self.log_info(f"第 {self.count} 次体力爬塔战斗结束 总共{self.ap_tickets}，下次休息{self.next_sleep_count}")
        self.Back_Home()


    def Battle_process(self):
        def check():
            if res := self.wait_feature('Event_Finish', threshold=0.7,
                                    box=self.box_of_screen(0.28, 0.15, 0.71, 0.63),
                                        raise_if_not_found=False,
                                        time_out=1):
                self.sleep(2)
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                    self.log_info("点击上面")
                else:
                    self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                    self.log_info("点击下面")
                self.sleep(2)
                if res1 := self.find_one('Event_Finish', threshold=0.7,
                                    box=self.box_of_screen(0.28, 0.15, 0.71, 0.63)):
                    self.sleep(2)
                    if random.randint(1, 2) == 1:
                        self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                        self.log_info("点击上面")
                    else:
                        self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                        self.log_info("点击下面")
                    self.sleep(0.5)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            if res := self.find_one('Event_Finish_2', threshold=0.7,
                                        box=self.box_of_screen(0.28, 0.15, 0.71, 0.63)):
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                    self.log_info("点击上面")
                else:
                    self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                    self.log_info("点击下面")
                self.sleep(2)
                if res1 := self.find_one('Event_Finish_2', threshold=0.7,
                                         box=self.box_of_screen(0.28, 0.15, 0.71, 0.63)):
                    if random.randint(1, 2) == 1:
                        self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                        self.log_info("点击上面")
                    else:
                        self.click_rect_random((0.3, 0.03, 0.69, 0.28))
                        self.log_info("点击下面")
                    self.log_info("第一次没点到")
                    self.sleep(1)
                    return True
                else:
                    self.log_info("第一次点到")
                    return True

        if self.config["Lock Team Enable"] and self.count == 2:
            self.log_info("进入第二次战斗锁住阵容")
            self.Lock_team((0.66, 0.88, 0.72, 0.99), lock=True)

        if text := self.wait_ocr(match=re.compile("挑战"),
                                 box=self.box_of_screen(0.87, 0.8, 0.96, 0.95)):
            self.click_rect_random((0.88, 0.82, 0.96, 0.94))
        if self.count == 1:
            self.log_info("进入检测1")
            if self.config["Lock Team Enable"]:
                self.Change_team(self.group, self.team)

            self.log_info("检测是否为自动")
            self.change_auto(self.green,self.GreenNum)
        else:
            self.click_green(self.GreenNum)

        if self.wait_until(check, time_out=self.BattleTime, settle_time=0, raise_if_not_found=False):
            return True

        
