import re
import random
from datetime import datetime, timedelta
from src.tasks.BaseBattleTask import BaseBattleTask
from datetime import datetime, timedelta
class TrueOrochiTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "周常-战斗-真八岐大蛇"
        self.description = "在打真蛇之前，最好在暴食鬼设置将五星及以下的御魂丢弃，避免御魂遮挡ui"
        self.default_config.update({
            "UserStatus": "队长",
            "Friend 1": "",
            "Friend 2": "",
        })
        self.config_description.update({
            "UserStatus": "队伍角色：队长创建的队伍，队员加入队伍，单人独自挑战。",
            "Friend 1": "邀请几位就填几位，不邀请请不要填写",
            "Green Enable": "是否绿标，真八岐大蛇从左到右填写1-7，7为阴阳师，0为不绿标"
        })
        self.config_type.update({
            "UserStatus": {
                "type": "drop_down",
                "options": ["队长", "队员", "单人"],
            },
            "FindMode": {
                "type": "drop_down",
                "options": ["好友", "跨区", "寮友"],
            },
        })
        self.green = {
            1: (0.19, 0.62),
            2: (0.26, 0.77),
            3: (0.39, 0.62),
            4: (0.56, 0.63),
            5: (0.67, 0.71),
            6: (0.75, 0.54),
            7: (0.48, 0.84),
        }

    def run(self):
        self.in_home_and_back()
        self.group, self.team = self._switch_preset_by_soul_zone()
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        if self.config["UserStatus"] == "队长":
            if not self.trueorochi_page():
                self.log_warning("SoulZones_page 失败")
                return False
            if not self.Leader_page():
                self.log_warning("Leader_page 失败")
                return False
            if not self.Invitation():
                self.log_warning("Invitation 失败")
                return False
            self.log_info("进入battle")
            self.Leader_battle()
            return True

    def trueorochi_page(self):
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        self.info_set("步骤", "进入探索页面")
        if self.wait_click_feature('Trueorochi', threshold=0.7,
                                        box=self.box_of_screen(0.01, 0.13, 0.11, 0.34),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("探索八岐大蛇")
        if self.wait_click_feature('Trueorochi_Attack_Ocr', threshold=0.7,
                                        box=self.box_of_screen(0.74, 0.64, 0.85, 0.86),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击挑战")
        else:
            return False
        if self.wait_click_feature('Confirm_Ocr', threshold=0.7,
                                   box=self.box_of_screen(0.5, 0.52, 0.69, 0.68),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击确定")
        if self.wait_click_feature('Private_Ocr', threshold=0.7,
                                   box=self.box_of_screen(0.3, 0.53, 0.52, 0.66),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击不公开")
        if self.wait_click_feature('Create_Ocr', threshold=0.7,
                                   box=self.box_of_screen(0.41, 0.65, 0.6, 0.78),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击创建")
        return True

    def invitation(self):
        if text := self.wait_ocr(match = re.compile("协战|队伍"),
                                  box=self.box_of_screen(0, 0, 0.17, 0.1), time_out=6):
            self.log_info(f"OCR: {text}")

        targets = [self.config["Friend 1"]]
        if self.config["Friend 2"]:
            targets.append(self.config["Friend 2"])

        for i, f in enumerate(targets):
            if i == 0:
                ok = self._invite_one(f, (0.50, 0.34), (0.43, 0.15, 0.53, 0.19),findmode=self.config["FindMode"],
                                      base_tabs=["好友", "跨区", "寮友"])
            else:
                ok = self._invite_one(f, (0.83, 0.34), (0.77, 0.14, 0.88, 0.19),findmode=self.config["FindMode"],
                                      base_tabs=["好友", "跨区", "寮友"])
            if not ok:
                return False
        return True
    def leader_battle(self):
        if self.wait_click_feature('Challenge_Featrue', threshold=0.7,
                                   box=self.box_of_screen(0.89, 0.78, 1, 1),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("点击挑战")
        return True
    def Find_finish(self, battle_time, success_box='Battle_Success'):
        """
        等待战斗结束并处理结算画面。

        Returns:
            1  战斗成功
            2  战斗失败
            3  超时
        """
        result = 1

        def finish():
            if res := self.wait_feature('Battle_Finish', threshold=0.7,
                                        box=self.B('Battle_Finish'),
                                        raise_if_not_found=False, time_out=6):
                self.sleep(0.5)
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.18, 0.05, 0.9, 0.21))
                else:
                    self.click_rect_random(res)

                if res1 := self.find_one('Battle_Finish', threshold=0.7,
                                          box=self.B('Battle_Finish')):
                    self.click(res1, after_sleep=0.1)
                    self.click(res1, after_sleep=0.1)
                    self.click(res1, after_sleep=0.1)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                return True
            elif res :=self.wait_feature('Battle_Finish_Soul', threshold=0.7,
                                        box=self.B('Battle_Finish_Soul'),
                                        raise_if_not_found=False, time_out=6):
                self.sleep(1)
                if random.randint(1, 2) == 1:
                    self.click_rect_random((0.18, 0.05, 0.9, 0.21))
                else:
                    self.click_rect_random(res)
                if res1 := self.find_one('Battle_Finish_Soul', threshold=0.7,
                                          box=self.B('Battle_Finish_Soul')):
                    self.click(res1, after_sleep=0.1)
                    self.click(res1, after_sleep=0.1)
                    self.click(res1, after_sleep=0.1)
                    self.log_info("第一次没点到")
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            return False

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
                else:
                    self.log_info("第一次点到")
                if finish():
                    return True
                else:
                    return False
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
                else:
                    self.log_info("第一次点到")
                if finish():
                    return True
                else:
                    return False
            if res := self.find_one('Battle_Finish', threshold=0.7,
                                        box=self.B('Battle_Finish')):
                self.click_rect_random(res)
                self.sleep(1)
                if res1 := self.find_one('Battle_Finish', threshold=0.7,
                                          box=self.B('Battle_Finish')):
                    self.click_rect_random(res1)
                    self.log_info("第一次没点到")
                    self.sleep(1)
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            if res := self.find_one('Battle_Finish_Soul', threshold=0.7,
                                        box=self.B('Battle_Finish_Soul')):
                self.click(res)
                self.sleep(1)
                if res1 := self.find_one('Battle_Finish_Soul', threshold=0.7,
                                          box=self.B('Battle_Finish_Soul')):
                    self.click(res1)
                    self.log_info("第一次没点到")
                    self.sleep(1)
                    return True
                else:
                    self.log_info("第一次点到")
                    return True
            if res := self.find_one('Battle_Failure', threshold=0.9,
                                        box=self.B('Battle_Failure')):
                self.click_rect_random(res)
                self.sleep(0.5)
                if res1 := self.find_one('Battle_Failure', threshold=0.9,
                                        box=self.B('Battle_Failure')):
                    self.click_rect_random(res1)
                    self.log_info("第一次没点到")
                    self.sleep(1)
                    result = 2
                    return True
                else:
                    self.log_info("第一次点到")
                    result = 2
                    return True
            return False

        if self.wait_until(check, time_out=battle_time, settle_time=0, raise_if_not_found=False):
            return result

        self.log_warning("战斗结束超时")
        return 3
    def battle(self):
        if self.wait_click_feature('Ready_Ocr', threshold=0.7,
                                   box=self.box_of_screen(0.84, 0.71, 0.99, 0.97),
                                   raise_if_not_found=False, time_out=10, after_sleep=1):
            self.log_info("点击准备")
        else:
            self.log_warning("没有准备")
            return False
        if self.wait_click_feature('Trueorochi_Auto_Ready', threshold=0.7,
                                   box=self.box_of_screen(0.83, 0.57, 0.99, 0.72),
                                   raise_if_not_found=False, time_out=10, after_sleep=1):
            self.log_info("点击自动准备,开始战斗")
        else:
            self.log_warning("没有自动准备")
            return False
        self.log_info("检测是否为自动")
        self.change_auto(self.green, self.GreenNum)

        res = self.Find_finish(self.BattleTime)
        if res == 2:
            self.log_warning("战斗失败！！")
            return False
        elif res == 3:
            self.log_warning("战斗超时！！")
            return False


