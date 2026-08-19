import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask

from datetime import datetime

class GameEventsBattleTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "活动-战斗-当期爬塔"
        self.description = "2026.8.19洛天依联动爬塔"
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
        self.click_rect_random((0.33, 0.34, 0.4, 0.45))
        self.sleep(1)
        if self.wait_click_ocr(match=re.compile("神威|破障|战斗"),
                             time_out=3,
                             box=self.box_of_screen(0.46, 0.5, 0.54, 0.84),
                             raise_if_not_found=False):
            self.log_info("进入战斗")
            return True
        elif self.wait_ocr(match=re.compile("获得|奖励"),
                           time_out=3,
                           box=self.box_of_screen(0.37, 0.24, 0.63, 0.39),
                           raise_if_not_found=False):
            self.sleep(0.5)
            self.click_rect_random((0.86, 0.25, 0.89, 0.31))
            self.sleep(1)
            self.click_rect_random((0.86, 0.25, 0.89, 0.31))
            if self.wait_click_ocr(match=re.compile("神威|破障|战斗"),
                                   time_out=3,
                                   box=self.box_of_screen(0.46, 0.5, 0.54, 0.84),
                                   raise_if_not_found=False):
                self.log_info("进入战斗")
                return True
        else:
            self.log_warning("没有进入战斗页面")
            return False

    def Battle(self):
        if self.wait_ocr(match=re.compile("养成|协战|式神"),
                         time_out=3,
                         box=self.box_of_screen(0.65,0.82,0.84,0.9)):
            self.sleep(0.5)
            if self.ocr(match=re.compile("必定|双倍|掉落"),
                             box=self.box_of_screen(0.01, 0.75, 0.32, 0.88)):
                self.log_info("现在是体力模式")
                self.isap = True
            else:
                self.log_info("现在是爬塔模式")
                self.isap = False
        else:
            self.log_warning("没有进入战斗页面")
            return False
        if not self.config["IsOcr"]:
            self.ap_tickets = int(self.config["ApTickets"])
            self.general_tickets = int(self.config["GeneralTickets"])
            self.log_info(f"体力爬塔票数{self.ap_tickets}")
            self.log_info(f"普通爬塔票数：{self.general_tickets}")
        else:
            if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.43, 0.03, 0.49, 0.09)):
                nums = re.findall(r'\d+', text[0].name)
                self.general_tickets = int(nums[0]) if nums else 0
                self.log_info(f"普通爬塔票数：{self.general_tickets}")

            if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.75, 0.03, 0.8, 0.09)):
                nums = re.findall(r'\d+', text[0].name)
                self.ap_tickets = int(nums[0]) if nums else 0
                self.log_info(f"体力爬塔票数{self.ap_tickets}")

        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.61, 0.89, 0.66, 0.97), lock=False)
        else:
            # 不换
            self.Lock_team((0.61, 0.89, 0.66, 0.97), lock=True)


        if self.config["GeneralClimb"]:
            self.count = 0
            self.log_info(self.count_range)
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
                self.log_info(f"下次休息{self.next_sleep_count}")
            if self.isap:
                self.click_rect_random((0.97, 0.76, 0.99, 0.79))
                self.log_info("切换为体力爬塔")
                self.isap = False
                self.sleep(0.5)
            else:
                self.log_info("爬塔")
            while self.count < self.general_tickets:
                self.Battle_process()
                self.count += 1
                if self.is_sleep:
                    self.log_info(f"会在第{self.next_sleep_count}次休息")
                    if self.count >= self.next_sleep_count:
                        self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                        a = random.randrange(*(self.time_range))
                        self.log_info(f"第 {self.count} 次爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                        self.sleep(a)
                self.log_info(f"第 {self.count} 次爬塔战斗结束 总共{self.general_tickets}，下次休息{self.next_sleep_count}")

        if self.config["ApMode"]:
            self.count=0
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
            if not self.isap:
                self.click_rect_random((0.97, 0.76, 0.99, 0.79))
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
            if res := self.wait_feature('Battle_Finish', threshold=0.7,
                                    box=self.B('Battle_Finish'),
                                        raise_if_not_found=False,
                                        time_out=1):
                self.sleep(2)
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.18, 0.77, 0.88, 0.95))
                    self.log_info("点击上面")
                else:
                    self.click_rect_random(res)
                    self.log_info("点击下面")
                self.sleep(2)
                if res1 := self.find_one('Battle_Finish', threshold=0.7,
                                    box=self.B('Battle_Finish')):
                    self.sleep(2)
                    if random.randint(1, 2) == 1:
                        self.click_rect_random((0.18, 0.05, 0.9, 0.21))
                    else:
                        self.click_rect_random(res1)
                    self.sleep(0.5)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            if res := self.find_one('Battle_Finish_Soul', threshold=0.7,
                                        box=self.B('Battle_Finish_Soul')):
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.18, 0.77, 0.88, 0.95))
                    self.log_info("点击上面")
                else:
                    self.click_rect_random(res)
                    self.log_info("点击下面")
                self.sleep(1)
                if res1 := self.find_one('Battle_Finish_Soul', threshold=0.7,
                                        box=self.B('Battle_Finish_Soul')):
                    self.click_rect_random((0.18, 0.05, 0.9, 0.21))
                    self.log_info("第一次没点到")
                    self.sleep(1)
                    return True
                else:
                    self.log_info("第一次点到")
                    return True

        if self.config["Lock Team Enable"] and self.count == 2:
            self.log_info("进入第二次战斗锁住阵容")
            self.Lock_team((0.14, 0.82, 0.2, 0.9), lock=True)

        if text := self.wait_ocr(match=re.compile("挑战"),
                                 box=self.box_of_screen(0.88,0.83,0.95,0.91)):
            self.click_rect_random((0.88, 0.8, 0.96, 0.92))
        if self.count == 1:
            self.log_info("进入检测1")
            if self.config["Lock Team Enable"]:
                self.Change_team(self.group, self.team)

            self.log_info("检测是否为自动")
            self.change_auto(self.GreenNum)
        else:
            self.click_green(self.GreenNum)

        if self.wait_until(check, time_out=self.BattleTime, raise_if_not_found=False):
            return True

        
