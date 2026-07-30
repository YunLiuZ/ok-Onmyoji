import re

from src.tasks.BuffBattleTask import BuffBattleTask


class AwakeTask(BuffBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "战斗-觉醒"


        self.default_config.update({
            "UserStatus": "队长",
            "Friend 1": "",
            "Friend 2": "",
            "Awake": "火",
        })
        self.config_description.update({
            "UserStatus": "队伍角色：队长创建的队伍，队员加入队伍，单人独自挑战。",
            "Friend 1": "邀请几位就填几位，不邀请请不要填写",
        })
        self.config_type.update({
            "Awake": {
                "type": "drop_down",
                "options": ["火", "风", "水", "雷"],
            },
        })
    def run(self):
        self.in_home_and_back()
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)

        if self.config["UserStatus"] == "队长":
            if not self.awake_page():
                self.log_warning("SoulZones_page 失败")
                return False
            if not self.leader_page():
                self.log_warning("Leader_page 失败")
                return False
            if not self.invitation():
                self.log_warning("Invitation 失败")
                return False
            self.log_info("进入battle")
            self.leader_battle()
            return True

        elif self.config["UserStatus"] == "单人":
            if not self.awake_page():
                self.log_warning("SoulZones_page 失败")
                return False
            self.Alone_battle()
            return True
        else:  # 队员
            if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                           box=self.B('Home_Explore'),
                                           raise_if_not_found=False, time_out=6, after_sleep=1):
                self.log_warning("找不到探索 Home_Sign")
            self.info_set("步骤", "进入探索页面")

            if self.open_buff(self.config.get("加成选择", [])):
                self.log_info("open buff")
            else:
                self.log_info("not open buff")

            self.log_info("等待邀请")
            if self.wait_click_feature('Invitation_Confirm', threshold=0.7,
                                       box=self.B('Invitation_Confirm'),
                                       raise_if_not_found=False, time_out=300, after_sleep=1):
                if self.Member_battle():
                    return True
                else:
                    return False
            else:
                self.log_warning("等待邀请超时")
                return False
    def awake_page(self):
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        self.info_set("步骤", "进入探索页面")

        if self.open_buff(self.config.get("加成选择", [])):
            self.log_info("open buff")
        else:
            self.log_info("not open buff")
        if self.wait_click_feature('Exploration_Awake', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("Exploration_Awake")
        elif text:=self.ocr_and_click(['觉醒','材料'],1,box=self.box_of_screen(0.03, 0.88, 0.11, 0.99)):
            self.log_info(f"OCR: {text}")
        else:
            self.log_info('找不到觉醒 ')
            return False

        if self.wait_ocr(match=re.compile("觉醒|之塔"), box=self.box_of_screen(0.11, 0, 0.17, 0.1)):
            if self.config["Awake"] == "火":
                self.click_relative(0.15,0.34)
                self.sleep(1)
            if self.config["Awake"] == "风":
                self.click_relative(0.4,0.34)
                self.sleep(1)
            if self.config["Awake"] == "水":
                self.click_relative(0.63,0.34)
                self.sleep(1)
            if self.config["Awake"] == "雷":
                self.click_relative(0.86,0.34)
                self.sleep(1)
        self._swipe(0.11, 0.69, 0.11, 0.22, 0.5)
        self._swipe(0.11, 0.69, 0.11, 0.22, 0.5)
        self.sleep(0.5)
        if text:=self.ocr_and_click('拾层',1,box=self.box_of_screen(0.06,0.43,0.16,0.94),time_out=6,):
                self.log_info('拾层')
                return True
        else:
            self.log_info('找不到十层')
            return False

    def leader_page(self):
        if self.ocr_and_click(['组队'], box=self.box_of_screen(0.74, 0.82, 0.83, 0.92)):
            self.log_info('点击组队')
        self.sleep(0.5)

        self.click_relative(0.84, 0.87, after_sleep=1)  # 组队

        if text := self.ocr_and_click(['不公开', '仅邀请', ], box=self.box_of_screen(0.61, 0.67, 0.78, 0.74)):
            self.log_info(f"OCR: {text}")
            self.click_relative(0.68, 0.80, after_sleep=1)
            return True
        return False
    def _invite_one(self, f: str, invite_xy: tuple, confirm_box: tuple) -> bool:
        """邀请单个好友：invite_xy=(x,y) 邀请按钮位置，confirm_box 确认区域。"""
        self.click_relative(*invite_xy, after_sleep=1)
        for tab in self._invite_tabs():
            if self.ocr_and_click(tab, box=self.B("Friend_Index")):
                if self.ocr_and_click(f, box=self.B("Friend")):
                    self.click_relative(0.60, 0.79, after_sleep=1)
                    self.log_info('寻找到一位')
                    if self.ocr_and_click(f, time_out=20,
                                           box=self.box_of_screen(*confirm_box)):
                        return True
        return False
    def invitation(self):
        if text := self.wait_ocr(['协战', '队伍'],
                                  box=self.box_of_screen(0, 0, 0.17, 0.1), time_out=6,):
            self.log_info(f"OCR: {text}")

        targets = [self.config["Friend 1"]]
        if self.config["Friend 2"]:
            targets.append(self.config["Friend 2"])

        for i, f in enumerate(targets):
            if i == 0:
                ok = self._invite_one(f, (0.50, 0.34), (0.43, 0.15, 0.53, 0.19))
            else:
                ok = self._invite_one(f, (0.83, 0.34), (0.77, 0.14, 0.88, 0.19))
            if not ok:
                return False
        return True

    def leader_battle(self):
        targets = [self.config["Friend 1"]]
        if self.config["Friend 2"]:
            targets.append(self.config["Friend 2"])

        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.01, 0.88, 0.05, 0.95), lock=False)
        else:
            # 不换
            self.Lock_team((0.01, 0.88, 0.05, 0.95), lock=True)

        self.count = 1

        while (self.count <= self.AttackNumber):
            for i, f in enumerate(targets):
                if i == 0:
                    ok = self.ocr_and_click(f, time_out=30, box=self.box_of_screen(0.43, 0.15, 0.53, 0.19))
                else:
                    ok = self.ocr_and_click(f, time_out=30, box=self.box_of_screen(0.77, 0.14, 0.88, 0.19))
                if ok:
                    self.click_relative(0.95, 0.90, after_sleep=0.5)
                    self.log_info("进入battle")

                    if self.count == 1:
                        self.log_info("进入检测1")
                        if self.config["Lock Team Enable"]:
                            self.Change_team(self.group, self.team)

                        self.log_info("检测是否为自动")
                        self.change_auto()
                    if self.GreenNum != 0:
                        if self.wait_ocr(
                                match=re.compile('自动'),
                                box=self.box_of_screen(0.02, 0.88, 0.08, 0.96),
                                time_out=8
                        ):
                            self.sleep(0.1)
                            x, y = self.green[self.GreenNum]
                            self.click_relative(x, y, after_sleep=1)

                    res = self.Find_finish(self.BattleTime)
                    if res == 2:
                        self.log_warning("战斗失败！！")
                        return False
                    elif res == 3:
                        self.log_warning("战斗超时！！")
                        return False
                    if self.count == 1:
                        if  self.wait_click_feature('Leader_Invitation', threshold=0.7,
                                            box=self.B('Leader_Invitation'),
                                            raise_if_not_found=False, time_out=6, after_sleep=1):
                            if not (self.ocr_and_click('确定',time_out=6,box=self.box_of_screen(0.51,0.53,0.67,0.63))):
                                self.log_warning("找不到确定")
                        else:
                            self.log_warning("找不到Leader_Invitation")

                    self.log_info(
                        f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
                    self.count += 1
                    self.trigger_count += 1
                else:
                    self.log_info("队友不在了")
                    self.Back_Home()
                    return False
        if not self.wait_click_feature('Back', threshold=0.7,
                                       box=self.B('Back'),
                                       raise_if_not_found=False, time_out=5, after_sleep=1):
            self.log_warning("找不到Battle_Finish")
        if self.ocr_and_click("确定", box=self.box_of_screen(0.54, 0.57, 0.63, 0.62)):
            self.wait_click_feature("Home_Button", box=self.B("Home_Button"), threshold=0.8, time_out=6, after_sleep=2)
        if self.in_home_and_back():
            return True
        else:
            return False
    def Member_battle(self):
        self.count = 1
        if self.config["Lock Team Enable"]:
            # 解锁状态 准备换队伍
            self.Lock_team((0.01, 0.88, 0.05, 0.95), lock=False)
        else:
            # 不换
            self.Lock_team((0.01, 0.88, 0.05, 0.95), lock=True)
        while self.count <= self.AttackNumber :
            if self.count == 1:
                self.log_info("进入检测1")
                if self.config["Lock Team Enable"]:
                    self.Change_team(self.group, self.team)

                self.log_info("检测是否为自动")
                self.change_auto()
            if self.GreenNum != 0:
                if self.wait_ocr(
                        match=re.compile('自动'),
                        box=self.box_of_screen(0.02, 0.88, 0.08, 0.96),
                        time_out=8
                ):
                    self.sleep(0.1)
                    x, y = self.green[self.GreenNum]
                    self.click_relative(x, y, after_sleep=1)

            res = self.Find_finish(self.BattleTime)
            if res == 2:
                self.log_warning("战斗失败！！")
                return False
            elif res == 3:
                self.log_warning("战斗超时！！")
                return False
            if self.count == 1:
                if not self.wait_click_feature('Member_Confirm', threshold=0.7,
                                        box=self.B('Member_Confirm'),
                                        raise_if_not_found=False, time_out=10, after_sleep=1):
                    self.log_warning("找不到Member_Confirm")
                if  self.wait_click_feature('Leader_Invitation', threshold=0.7,
                                        box=self.B('Leader_Invitation'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
                        if not (self.ocr_and_click('确定',time_out=6,box=self.box_of_screen(0.45,0.45,0.70,0.70))):
                            self.log_warning("找不到确认")
            self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
            self.count += 1
            self.trigger_count+=1
        if self.Back_Home():
            return True
        else:
            return False
    def Alone_battle(self):
        pass

