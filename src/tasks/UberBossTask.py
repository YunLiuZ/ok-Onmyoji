import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class UberBossTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "活动-战斗-超鬼王"
        self.description = "2026.11.11超鬼王,暂时只支持一只四星鬼王的普通战斗，并且只支持一套阵容打所有Boss"
        self.default_config.update({
            "Tickets":"0,0,0,0,0,0",
            "Level":"4",
        })
        self.config_description.update({
            "ApTickets": "当前拥有鬼王票数量",
            "Level": "自动打多少星以下的鬼王",
        })
        self.green = {
            1: (0.19, 0.75),
            2: (0.32, 0.68),
            3: (0.45, 0.68),
            4: (0.58, 0.71),
            5: (0.71, 0.8),
            6: (0.44, 0.86),
        }
        self.ap = 0
        self.one = 0
        self.two = 0
        self.three = 0
        self.four = 0
        self.five = 0
        self.six = 0
        self.level = 0
        self.battle_mode = "consume"
    def run(self):
        self.in_home_and_back()
        self.level = int(self.config["Level"])
        self.is_sleep,self.count_range , self.time_range = self._random_sleep(self.config["RandomSleep"])
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        self.one,self.two,self.three,self.four,self.five,self.six = self._parse_preset(self.config["Tickets"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        self.page()
        self.battle()

    def get_ap(self):
        if self.wait_ocr(match=re.compile("祸主|降临"),
                         time_out=6,
                         box=self.box_of_screen(0.08, 0.01, 0.25, 0.12),
                         raise_if_not_found=False):
            self.log_info("超鬼王页面")
        else:
            return False

        if text := self.wait_ocr(threshold=0.8,box=self.box_of_screen(0.84, 0.01, 0.97, 0.1),
                                 time_out=6):
            nums = re.findall(r'\d+', text[0].name)
            self.ap = int(nums[0]) if nums else 0
            self.log_info(f"当前体力值为：{self.ap}")
            return True
        else:
            return False

    def page(self):
        self.click_rect_random((0.35, 0.35, 0.38, 0.4))
        if self.wait_ocr(match=re.compile("祸主|降临|鬼王"),
                         time_out=3,
                         box=self.box_of_screen(0.68, 0.04, 0.81, 0.41),
                         raise_if_not_found=False):
            self.sleep(2)
            self.click_rect_random((0.69, 0.06, 0.8, 0.38))
        if self.wait_ocr(match=re.compile("祸主|降临"),
                         time_out=3,
                         box=self.box_of_screen(0.08, 0.01, 0.25, 0.12),
                         raise_if_not_found=False):
            self.log_info("进入超鬼王页面")
        else:
            return False
        self.get_ap()

    def select_boss(self):
        # 进入恢复模式
        if self.battle_mode == "consume" and self.ap >= 90:
            self.battle_mode = "recover"
            self.log_info("体力消耗达到90，进入恢复模式")

        # 恢复模式退出条件
        if self.battle_mode == "recover":
            if self.ap <= 50 or self.four <= 0 or self.level < 4:
                self.battle_mode = "consume"
                self.log_info("体力恢复到阈值或四星票数耗尽，退出恢复模式")

        # 恢复模式：优先打四星
        if self.battle_mode == "recover":
            if self.ap <= 90 and self.four > 0:
                return 4

            return None

        # 消耗模式：优先三星、二星、一星
        costs = {3: 5, 2: 7, 1: 9}
        tickets = {
            3: self.three,
            2: self.two,
            1: self.one
        }

        for star in (3, 2, 1):
            if (
                    self.level >= star
                    and tickets[star] > 0
                    and self.ap + costs[star] <= 90
            ):
                return star

        # 低星无法继续挑战，切换四星
        if self.level >= 4 and self.four > 0 and self.ap <= 90:
            self.battle_mode = "recover"
            self.log_info("低星暂时无法挑战，切换四星恢复体力")
            return 4

        return None

    def fight_boss(self, star):
        boss_features = {
            1: "Boss_One",
            2: "Boss_Two",
            3: "Boss_Three",
            4: "Boss_Four",
        }

        ticket_attrs = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
        }

        if star not in boss_features:
            return False

        attr = ticket_attrs[star]

        # 判断是否还有票
        if getattr(self, attr) <= 0:
            self.log_info(f"{star}星鬼王票数不足")
            return False
        if self.wait_ocr(match=re.compile("召唤|鬼王"),
                         time_out=15,
                         box=self.box_of_screen(0.87, 0.79, 0.98, 0.96),
                         raise_if_not_found=False):
            self.sleep(2)
            self.log_info("未发现鬼王")
        if self.wait_click_ocr(match=re.compile("全部|队列"),
                               time_out=3,
                               box=self.box_of_screen(0.85, 0.68, 0.99, 0.75),
                               raise_if_not_found=False):
            self.log_info("点击鬼王选择")
        else:
            self.log_info("没有寻找到鬼王选择")

        # 1. 选择鬼王
        if self.wait_click_feature(
                boss_features[star],
                time_out=6,
                threshold=0.95,
                box=self.box_of_screen(0.25, 0.37, 0.76, 0.62),
                raise_if_not_found=False
        ):
            self.log_info(f"寻找到对应{star}星鬼王")
        else:
            self.log_info(f"未找到对应{star}星鬼王")
            return False
        self.sleep(1)

        # 2. 立即召唤
        self.click_rect_random((0.45, 0.63, 0.55, 0.68))

        # 3. 等待挑战界面
        if not self.wait_click_ocr(
                match=re.compile("挑战"),
                time_out=3,
                box=self.box_of_screen(0.87, 0.79, 0.98, 0.96),
                raise_if_not_found=False
        ):
            self.log_info("未进入挑战界面")
            return False

        self.sleep(2)
        self.log_info(f"开始挑战{star}星鬼王")

        # 4. 点击预设并准备
        if not self.wait_ocr(
                match=re.compile("预设"),
                box=self.box_of_screen(0.02, 0.87, 0.14, 1.0),
                raise_if_not_found=False,
                time_out=6
        ):
            self.log_info("未找到预设")
            return False

        self.sleep(2)
        self.click_rect_random((0.88, 0.75, 0.95, 0.85))

        # 5. 等待战斗成功
        if self.wait_feature(
                "Battle_Success",
                time_out=self.BattleTime,
                threshold=0.8,
                box=self.box_of_screen(0.29, 0.06, 0.47, 0.34),
                raise_if_not_found=False
        ):
            self.sleep(2)
            self.click_rect_random((0.35, 0.16, 0.42, 0.27))
        else:
            self.log_info(f"{star}星鬼王战斗未确认成功")
            return False

        self.sleep(1)

        # 6. 再次尝试点击战斗成功界面
        if self.wait_feature(
                "Battle_Success",
                time_out=3,
                threshold=0.8,
                box=self.box_of_screen(0.29, 0.06, 0.47, 0.34),
                raise_if_not_found=False
        ):
            self.click_rect_random((0.35, 0.16, 0.42, 0.27))
            self.log_info("第一次没点到")
        else:
            self.log_info("第一次点到")

        # 7. 更新剩余票数
        remaining = getattr(self, attr) - 1
        setattr(self, attr, remaining)

        self.log_info(f"{star}星鬼王战斗结束，剩余票数：{remaining}")

        # 8. 重新识别体力
        self.sleep(4)
        if self.get_ap():
            self.log_info("体力识别成功")
        else:
            self.log_info("体力识别失败")
        return True

    def battle(self):
        while True:
            star = self.select_boss()

            if star is None:
                self.log_info("当前没有满足条件的鬼王")
                break

            if not self.fight_boss(star):
                self.log_info(f"{star}星鬼王战斗失败")
                break









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
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
            if self.isap:
                self.click_rect_random((0.91, 0.75, 0.93, 0.78))
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
                        self.log_info(f"第 {self.count} 次体力爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                        self.sleep(a)
                self.log_info(f"第 {self.count} 次体力爬塔战斗结束")
        if self.config["ApMode"]:
            if not self.wait_ocr(match=re.compile("修行|合训"),
                                       time_out=6,
                                       raise_if_not_found=False):
                self.log_warning("没有进入战斗")
            self.count = 0
            if self.is_sleep:
                self.next_sleep_count = random.randrange(*(self.count_range))
            if not self.isap:
                self.click_rect_random((0.91, 0.75, 0.93, 0.78))
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
                        self.log_info(f"第 {self.count} 次体力爬塔战斗结束,休息{a}秒，下次休息{self.next_sleep_count}")
                        self.sleep(a)
                self.log_info(f"第 {self.count} 次体力爬塔战斗结束")
        self.Back_Home()

    def Battle_process(self):
        if self.wait_ocr(match=re.compile("尚未|发现"),
                                   box=self.box_of_screen(0.04, 0.54, 0.15, 0.62),
                                   time_out=3,
                                   raise_if_not_found=False):
            self.log_info("没有发现御灵")

            if self.wait_ocr(match=re.compile("搜寻"),
                                       box=self.box_of_screen(0.83, 0.79, 0.94, 0.93),
                                       time_out=3,
                                       raise_if_not_found=False):
                self.click_rect_random((0.85, 0.8, 0.94, 0.92))
        else:
            self.click_rect_random((0.09, 0.18, 0.22, 0.26))
            self.log_info("发现御灵")

        if text := self.wait_ocr(match=re.compile("挑战"),
                                       box=self.box_of_screen(0.86, 0.72, 0.94, 0.9)):
            self.log_info(f"OCR: {text},进入战斗")
        # self.sleep(1)
        # self.click_relative(random.uniform(0.705, 0.745), random.uniform(0.827, 0.883))
        # self.sleep(1)
        # self.click_relative(random.uniform(0.639, 0.711), random.uniform(0.725, 0.765))
        self.Lock_team((0.85, 0.6, 0.93, 0.68), lock=True)
        if self.wait_ocr(match=re.compile("挑战"),
                                       box=self.box_of_screen(0.86, 0.72, 0.94, 0.9),
                                   time_out=6,
                                   raise_if_not_found=False):
            self.click_rect_random((0.86, 0.74, 0.93, 0.86))
        else:
            self.log_info("找不到战斗按钮")
            return False
        self.log_info("检测是否为自动")
        if self.count == 1:
            self.log_info("进入检测1")
            self.log_info("检测是否为自动")
            self.change_auto(self.green,self.GreenNum)
        else:
            self.click_green(self.green,self.GreenNum)
        fail_count = 0
        while fail_count < 2:
            result = 1
            def check():
                nonlocal result
                if self.wait_feature('Battle_Success', threshold=0.9,
                                                   box=self.B('success_box'),
                                                    raise_if_not_found=False, time_out=1,):
                    self.log_info("战斗成功")
                    result = 1
                    self.sleep(0.2)
                    self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                    if res1 := self.find_one('Battle_Success', threshold=0.95,
                                                              box=self.B('success_box')):
                        self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                        self.sleep(0.5)
                        self.log_info("第一次没点到")
                    else:
                        self.log_info("第一次点到")
                    return True
                if res := self.find_one('Battle_Failure', threshold=0.95,
                                        box=self.B('Battle_Failure')):
                    self.log_info("战斗失败")
                    result = 2
                    self.click_rect_random(res)
                    self.sleep(0.5)
                    if res1 := self.find_one('Battle_Failure', threshold=0.9,
                                             box=self.B('Battle_Failure')):
                        self.click_rect_random(res1)
                        self.log_info("第一次没点到")
                        self.sleep(1)
                        return True
                    else:
                        self.log_info("第一次点到")
                        return True
                return False

            if self.wait_until(check, time_out=self.BattleTime, settle_time=0, raise_if_not_found=False):
                if result == 1:
                    return True
                fail_count += 1
                self.log_warning(f"战斗失败，第 {fail_count} 次，重新挑战")
                if self.wait_ocr(match=re.compile("挑战"),
                                 box=self.box_of_screen(0.86, 0.72, 0.94, 0.9),
                                 time_out=6,
                                 raise_if_not_found=False):
                    self.click_rect_random((0.86, 0.74, 0.93, 0.86))
                self.sleep(1)
            else:
                self.log_warning("战斗结束超时")
                return False
        self.log_warning("失败超过2次")
        return False

