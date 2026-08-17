import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class UberBossTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "活动-战斗-超鬼王"
        self.description = "2026.8.12武道大会,每日清票,本任务暂时只支持打合训，爬塔暂时没写，并且只支持一套阵容打所有Boss"
        self.default_config.update({
            "ApMode": True,
            "GeneralClimb": True,
            "GeneralTickets":"0",
            "ApTickets":"0"
        })
        self.config_description.update({
            "ApMode": "注灵票战斗是否开启",
            "GeneralClimb": "普通票战斗是否开启",
            "Lock Team Enable":"考虑到借式神，暂时只支持一个预设队伍一直打，请手动设置每个boss的战斗队伍",
            "AttackNumber": "无需填写",
            "GeneralTickets": "普通票数量",
            "ApTickets": "注灵票数量"
        })
        self.green = {
            1: (0.19, 0.75),
            2: (0.32, 0.68),
            3: (0.45, 0.68),
            4: (0.58, 0.71),
            5: (0.71, 0.8),
            6: (0.44, 0.86),
        }

        self.general_tickets = 0
        self.ap_tickets = 0
        self.isap = True
    def run(self):
        self.in_home_and_back()
        self.is_sleep,self.count_range , self.time_range = self._random_sleep(self.config["RandomSleep"])
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        self.Battle_page()


    def Battle_page(self):
        self.click_relative(0.37,0.6,after_sleep=2)
        if not self.wait_click_ocr(match=re.compile("修行|合训"),
                               time_out=6,
                               raise_if_not_found=False):
            self.log_warning("没有进入战斗")
        if not self.wait_ocr(match=re.compile("修行|合训"),
                             time_out=3,
                             box=self.box_of_screen(0,0,0.2,0.2),
                             raise_if_not_found=False):
            self.log_warning("没有进入战斗页面")
            return False
        if text := self.ocr(match=re.compile("注灵"),
                            box=self.box_of_screen(0.83, 0.79, 0.94, 0.93)):
            self.log_info(f"OCR: {text}")
            self.log_info("现在是注灵模式")
            self.isap = True
        else:
            self.log_info(f"OCR: {text}")
            self.log_info("现在是爬塔模式")
            self.isap = False
        self.ap_tickets = int(self.config["ApTickets"])
        self.general_tickets = int(self.config["GeneralTickets"])
        self.log_info(f"普通搜索票数：{self.general_tickets}")
        self.log_info(f"注灵搜索的票数{self.ap_tickets}")
        # if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.76, 0.02, 0.79, 0.06)):
        #     nums = re.findall(r'\d+', text[0].name)
        #     self.general_tickets = int(nums[0]) if nums else 0
        #     self.log_info(f"普通搜索票数：{self.general_tickets}")
        # if text := self.ocr(threshold=0.8,box=self.box_of_screen(0.93, 0.03, 0.95, 0.06)):
        #     nums = re.findall(r'\d+', text[0].name)
        #     self.ap_tickets = int(nums[0]) if nums else 0
        #     self.log_info(f"注灵搜索的票数{self.ap_tickets}")
        if self.config["GeneralClimb"]:
            self.count = 0
            self.next_sleep_count = random.randrange(*(self.count_range))
            if self.isap:
                self.click_relative(0.92, 0.77)
                self.log_info("切换为爬塔")
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
                        self.sleep(a)
                        self.log_info(f"第 {self.count} 次体力爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                self.log_info(f"第 {self.count} 次体力爬塔战斗结束")
        if self.config["ApMode"]:
            if not self.wait_ocr(match=re.compile("修行|合训"),
                                       time_out=6,
                                       raise_if_not_found=False):
                self.log_warning("没有进入战斗")
            self.count = 0
            self.next_sleep_count = random.randrange(*(self.count_range))
            if not self.isap:
                self.click_relative(0.92, 0.77)
                self.log_info("切换为注灵爬塔")
                self.isap = True
                self.sleep(0.5)
            else:
                self.log_info("体力")
            while self.count < self.ap_tickets:
                self.log_info("123")
                self.Battle_process()
                self.count += 1
                if self.is_sleep:
                    self.log_info(f"会在第{self.next_sleep_count}次休息")
                    if self.count >= self.next_sleep_count:
                        self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                        a = random.randrange(*(self.time_range))
                        self.sleep(a)
                        self.log_info(f"第 {self.count} 次体力爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                self.log_info(f"第 {self.count} 次体力爬塔战斗结束")
        self.Back_Home()

    def Battle_process(self):
        if self.wait_click_ocr(match=re.compile("尚未|发现"),
                                   box=self.box_of_screen(0.04, 0.54, 0.15, 0.62),
                                   time_out=3,
                                   raise_if_not_found=False):
            self.log_info("没有发现御灵")
            if not self.wait_click_ocr(match=re.compile("搜寻"),
                                       box=self.box_of_screen(0.83, 0.79, 0.94, 0.93),
                                       time_out=3,
                                       raise_if_not_found=False):
                self.log_info("没有进入战斗")
        else:
            self.click_relative(0.06, 0.18)
            self.log_info("发现御灵")

        if text := self.wait_ocr(match=re.compile("挑战"),
                                       box=self.box_of_screen(0.86, 0.72, 0.94, 0.9)):
            self.log_info(f"OCR: {text},进入战斗")
        # self.sleep(1)
        # self.click_relative(random.uniform(0.705, 0.745), random.uniform(0.827, 0.883))
        # self.sleep(1)
        # self.click_relative(random.uniform(0.639, 0.711), random.uniform(0.725, 0.765))
        self.Lock_team((0.85, 0.6, 0.93, 0.68), lock=True)
        if not self.wait_click_ocr(match=re.compile("挑战"),
                                       box=self.box_of_screen(0.86, 0.72, 0.94, 0.9),
                                   time_out=6,
                                   raise_if_not_found=False):
            self.log_info("找不到战斗按钮")
            return False
        self.log_info("检测是否为自动")
        if self.count == 1:
            self.log_info("进入检测1")
            self.log_info("检测是否为自动")
            self.change_auto(self.GreenNum)
        else:
            self.click_green(self.GreenNum)
        if self.wait_click_feature('Battle_Success',threshold=0.9,
                                box=self.box_of_screen(0.24, 0.1, 0.83, 0.45),
                                raise_if_not_found=False,
                                time_out=self.BattleTime,):
            return True
        else:
            return False
