import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask

DUEL_RANKS = ["一段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "名仕"]


class DuelTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "周常-斗技"
        self.description = "名仕以下挂机，并且至少达到了轮训选式神的模式，自动点击自动上阵第一次打请手动设置好上阵顺序，如果长时间没有玩过斗技，请先手动玩一次斗技，消除弹窗"
        self.rank = 0 #斗技分数
        self.rank_num = 0 #斗技段数
        self.default_config.update({
            "Duel":"一段"
        })
        self.config_type.update({
            "Duel": {
                "type": "drop_down",
                "options": ["一段", "二段", "三段", "四段", "五段", "六段", "七段", "八段", "九段", "名仕"],
            },
        })
        self.config_description.update({
            "Duel":"此参数如果不是一段，那么就会一直挂机打斗技直到到达这个段数",
            "AttackNumber":"如果下方斗技参数是一段，那么就会按照战斗次数来检测打斗技的次数，如果你是每周拿斗技积分换蓝票，很适合用这个参数"
        })

        self.green = {
            1: (0.24, 0.56, 0.26, 0.64),
            2: (0.38, 0.52, 0.40, 0.57),
            3: (0.51, 0.51, 0.53, 0.56),
            4: (0.64, 0.52, 0.66, 0.57),
            5: (0.78, 0.58, 0.80, 0.65),
            6: (0.51, 0.69, 0.53, 0.73),
        }

    def _current_rank_idx(self):
        """OCR 检测当前段位，返回段位索引，识别不到返回 -1。"""
        res = self.wait_ocr(match=re.compile("|".join(DUEL_RANKS)),
                            time_out=3,
                            box=self.box_of_screen(0.42, 0.58, 0.58, 0.74),
                            raise_if_not_found=False)
        if res:
            text = "".join(r.name for r in res)
            for i, rank in enumerate(DUEL_RANKS):
                if rank in text:
                    return i
        return -1

    def run(self):
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        self.is_sleep, self.count_range, self.time_range = self._random_sleep(self.config["RandomSleep"])
        self.in_home_and_back()
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        self.duel_page()
        self.battle()
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
            self.log_warning("没找到斗技")
            return False
        self.click_rect_random((0.3, 0.05, 0.7, 0.18))#长时间不进入消除弹窗
    def Find_finish(self, battle_time, success_box='Battle_Success'):
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
            if self.wait_feature('Battle_Success', threshold=0.9,
                                               box=self.B('success_box'),
                                                raise_if_not_found=False, time_out=1,):
                self.sleep(0.2)
                self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                if res1 := self.find_one('Battle_Success', threshold=0.9,
                                                          box=self.B('success_box')):
                    self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                    self.sleep(0.5)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True

            if self.wait_feature('Battle_Failure', threshold=0.9,
                                               box=self.B('success_box'),
                                                raise_if_not_found=False, time_out=1,):
                self.sleep(0.2)
                self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                if res1 := self.find_one('Battle_Failure', threshold=0.9,
                                                          box=self.B('success_box')):
                    self.click_rect_random((0.1, 0.1, 0.9, 0.47))
                    self.sleep(0.5)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True

        if self.wait_until(check, time_out=battle_time, settle_time=0, raise_if_not_found=False):
            return result

        self.log_warning("战斗结束超时")
        return 3
    def battle(self):
        if self.is_sleep:
            self.next_sleep_count = random.randrange(*(self.count_range))
        target = self.config["Duel"]
        target_idx = DUEL_RANKS.index(target) if target in DUEL_RANKS else 0
        self.log_info(f"目标段位:{target}, 模式:{'按次数' if target_idx == 0 else '按段数'}")
        self.count = 1
        while True:
            if target_idx == 0:
                if self.count > self.AttackNumber:
                    break
            else:
                cur_idx = self._current_rank_idx()
                if cur_idx >= target_idx:
                    self.log_info(f"已达到目标段位 {target}，停止斗技")
                    break
            for i in range(3):
                if self.wait_ocr(match=re.compile("斗技"),
                                        time_out=3,
                                        box=self.box_of_screen(0, 0, 0.2, 0.2),
                                        raise_if_not_found=False, ):
                    self.log_info(f"进入战斗准备页面")
                    break
                else:
                    self.click_rect_random((0.44, 0.17, 0.55, 0.27))
                for i in range(5):
                    if not (res:=self.wait_ocr(match=re.compile("|".join(DUEL_RANKS)),
                             time_out=3,
                             box=self.box_of_screen(0.42, 0.58, 0.58, 0.74),
                             raise_if_not_found=False,)):
                        self.click_rect_random((0.24, 0.16, 0.77, 0.32))
                        self.sleep(1)
                        self.log_info("可能有弹窗")
                    self.log_info(f"当前的段位为{res}")
                    break
            self.sleep(1)
            self.click_rect_random((0.92, 0.81, 0.95, 0.88)) #start
            if not self.wait_click_feature('Duel_Auto_Choose', threshold=0.8,
                                           time_out=6, box=self.box_of_screen(0.0, 0.13, 0.08, 0.27),
                                           raise_if_not_found=False):
                self.log_warning("没有检测到自动上阵")
            if not self.wait_click_feature('Duel_Auto_Battle', threshold=0.8,
                                           time_out=120, box=self.box_of_screen(0.0, 0.74, 0.13, 0.99),
                                           raise_if_not_found=False):
                self.log_warning("没有检测到自动战斗")
            self.log_info("进入绿标")
            self.sleep(0.3)
            if self.GreenNum != 0:
                self.click_rect_random(self.green[self.GreenNum])
            if self.Find_finish(self.BattleTime) != 1:
                self.Back_Home()
                return False
            self.log_info(f"{self.count}次斗技战斗结束")
            self.count += 1
            if self.is_sleep:
                self.log_info(f"会在第{self.next_sleep_count}次休息")
                if self.count >= self.next_sleep_count:
                    self.next_sleep_count = self.count + random.randrange(*(self.count_range))
                    a = random.randrange(*(self.time_range))
                    self.log_info(f"第 {self.count} 次斗技结束,休息{a}秒，下次休息{self.next_sleep_count}")
                    self.sleep(a)
        self.Back_Home()
        return True




