import re

from src.tasks.BuffBattleTask import BuffBattleTask
class GoldYoukaiTask(BuffBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-战斗-金币妖怪"
        self.default_config.update({
            "UserStatus": "队长",
            "Friend 1": "",
            "Friend 2": "",
        })
        self.config_description.update({
            "UserStatus": "队伍角色：队长创建的队伍，队员加入队伍，单人独自挑战。",
            "Friend 1": "邀请几位就填几位，不邀请请不要填写",
        })
        self.config_type.update({
            "UserStatus": {
                "type": "drop_down",
                "options": ["队长", "队员", "单人"],
            },
        })
    def run(self):
        self.in_home_and_back()
        self.count = 1
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        while (self.count <= self.AttackNumber):
            if self.config["UserStatus"] == "队长":
                if not self.goldyoukai_page():
                    self.log_warning("找不到页面")
                    return False
                if not self.Invitation():
                    self.log_warning("Invitation 失败")
                    return False
                if not self.Leader_battle():
                    self.log_warning("Leader_page 失败")
                    return False
            elif self.config["UserStatus"] == "单人":
                if not self.goldyoukai_page():
                    self.log_warning("找不到页面")
                    return False
                self.Alone_battle()
                return True
            else:
                if self.config["加成选择"] and self.count==1:
                    if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                                   box=self.B('Home_Explore'),
                                                   raise_if_not_found=False, time_out=6, after_sleep=1):
                        self.log_warning("找不到探索 Home_Sign")
                    self.info_set("步骤", "进入探索页面")
                    if self.open_buff(self.config.get("加成选择", [])):
                        self.log_info("open buff")
                        self.Back_Home()
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
    def goldyoukai_page(self):
        if self.config["加成选择"] and self.count==1:
            if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                           box=self.B('Home_Explore'),
                                           raise_if_not_found=False, time_out=6, after_sleep=1):
                self.log_warning("找不到探索 Home_Sign")
            self.info_set("步骤", "进入探索页面")
            if self.open_buff(self.config.get("加成选择", [])):
                self.log_info("open buff")
                self.Back_Home()
        else:
            self.log_info("not open buff")
        if not self.wait_click_feature('Home_Team', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Team")
        self.log_info("进入组队页面")
        if self.wait_click_ocr(match=re.compile("金币"), threshold=0.7,
                                        box=self.box_of_screen(0.11, 0.18, 0.29, 0.87),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            
            self.log_info("金币妖怪")
        else:
            self._swipe(0.22,0.22,0.22,0.82,0.2)
            self.sleep(0.5)
            self.log_info("滑到顶")
            self._swipe(0.22,0.82,0.22,0.22,0.7)
            self.sleep(1)
            if self.wait_click_ocr(match=re.compile("金币"),
                                   box=self.box_of_screen(0.11, 0.18, 0.29, 0.87),
                                   raise_if_not_found=False, time_out=6,):
                self.sleep(0.5)
            else:
                self._swipe(0.22, 0.82, 0.22, 0.22, 0.7)
                if self.wait_click_ocr(match=re.compile("金币"),
                                       box=self.box_of_screen(0.11, 0.18, 0.29, 0.87),
                                       raise_if_not_found=False, time_out=6, ):
                    self.sleep(0.5)
                    self.log_warning("找不到金币妖怪")
                    return False
        
        if self.wait_click_ocr(re.compile("创建|队伍"), threshold=0.7,
                                        box=self.box_of_screen(0.74, 0.79, 0.94, 0.94),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.sleep(0.5)
            if self.wait_click_ocr(match=re.compile("不公开|仅邀请"), threshold=0.7,
                                   box=self.box_of_screen(0.3457, 0.5653, 0.5074, 0.6243)):
                self.sleep(0.5)
                self.click_relative(0.51,0.71,after_sleep=1)
                self.log_info("创建队伍")
            elif res :=self.ocr(re.compile("创建|队伍"), threshold=0.7,
                                        box=self.box_of_screen(0.74, 0.79, 0.94, 0.94)):
                self.click(res[0])
                self.log_info("出现弹窗 再次点击")
                self.wait_click_ocr(match=re.compile("不公开|仅邀请"), threshold=0.7,
                                    box=self.box_of_screen(0.3457, 0.5653, 0.5074, 0.6243))
                self.click_relative(0.51, 0.71, after_sleep=1)
                self.log_info("创建队伍")
        if text:=self.wait_ocr(match=re.compile("协战|队伍"),box=self.box_of_screen(0,0,0.2,0.1)):
            
          self.log_info('进入协战队伍')
          return True
        else:
          self.log_info('没有进入队伍')
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

    def Invitation(self):
        if text := self.wait_ocr(match=re.compile("协战|召回"),
                                  box=self.box_of_screen(0, 0, 0.17, 0.1), time_out=6):
            print(text)

        targets = [self.config["Friend 1"]]
        if self.config["Friend 2"]:
            targets.append(self.config["Friend 2"])

        for i, f in enumerate(targets):
            if i == 0:
                ok = self._invite_one(f, (0.33, 0.4), (0.22, 0.14, 0.42, 0.28))
            else:
                ok = self._invite_one(f, (0.52, 0.43), (0.42, 0.17, 0.61, 0.32))
            if not ok:
                return False
        return True
    def Leader_battle(self):
        targets = [self.config["Friend 1"]]
        if self.config["Friend 2"]:
            targets.append(self.config["Friend 2"])
        for i, f in enumerate(targets):
            if i == 0:
              ok = self.ocr_and_click(f, time_out=30,box=self.box_of_screen (0.22, 0.14, 0.42, 0.28))
            else:
              ok = self.ocr_and_click(f, time_out=30,box=self.box_of_screen (0.42, 0.17, 0.61, 0.32))
            if ok:
                self.click_relative(0.95, 0.90, after_sleep=0.5)
                self.log_info("进入battle")
                # 经验副本的success是独立的
                if self.config["Lock Team Enable"]:
                    self.Change_team(self.group, self.team)
                else:
                    if self.wait_ocr(match=re.compile("预设"),
                                     box=self.box_of_screen(0.02, 0.87, 0.14, 1.0),
                                     raise_if_not_found=False, time_out=60):
                        self.sleep(0.5)
                        self.click_relative(0.91, 0.79)
                if self.wait_until(condition=lambda: self.base_scene(),
                                   time_out=self.BattleTime,
                                   pre_action=lambda: self.wait_click_feature('Youkai_Success', threshold=0.7,
                                                                              box=self.box_of_screen(0.2, 0, 0.5, 0.43),
                                                                              raise_if_not_found=False,
                                                                              time_out=self.BattleTime,
                                                                              after_sleep=0.5),
                                   raise_if_not_found=False):
                    self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
                    self.count += 1
                    self.trigger_count += 1
                    return True
                else:
                    self.log_warning("没有检测到战斗结束")
                    return False
            else:
                self.log_info("队友不在了")
                self.Back_Home()
                return False
    def Alone_battle(self):
        self.sleep(0.5)
        self.click_relative(0.95, 0.90, after_sleep=0.5)
        # 金币副本的success是独立的
        if self.config["Lock Team Enable"]:
            self.Change_team(self.group, self.team)
        else:
            if self.wait_ocr(match=re.compile("预设"),
                             box=self.box_of_screen(0.02, 0.87, 0.14, 1.0),
                             raise_if_not_found=False, time_out=60):
                self.sleep(0.5)
                self.click_relative(0.91, 0.79)
        if self.wait_until(condition=lambda: self.base_scene(),
                           time_out=self.BattleTime,
                           pre_action=lambda: self.wait_click_feature('Youkai_Success', threshold=0.7,
                                                                      box=self.box_of_screen(0.2, 0, 0.5, 0.43),
                                                                      raise_if_not_found=False,
                                                                      time_out=self.BattleTime,
                                                                      after_sleep=0.5),
                           raise_if_not_found=False):
            self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
            self.count += 1
            self.trigger_count += 1
            return True
        else:
            self.log_warning("没有检测到战斗结束")
            return False
    def Member_battle(self):
        # 金币副本的success是独立的
        if self.config["Lock Team Enable"]:
            self.Change_team(self.group, self.team)

        elif self.wait_ocr(match=re.compile("预设"),
                             box=self.box_of_screen(0.02, 0.87, 0.14, 1.0),
                             raise_if_not_found=False, time_out=120):
                self.sleep(0.5)
                self.click_relative(0.91, 0.79)
        else:
            self.log_warning("没有检测到战斗页面")
            return False
        if self.wait_until(condition=lambda :self.base_scene(),
                           time_out=self.BattleTime,
                           pre_action=lambda :self.wait_click_feature('Youkai_Success', threshold=0.7,
                                   box=self.box_of_screen(0.2, 0, 0.5, 0.43),
                                   raise_if_not_found=False, time_out=self.BattleTime,
                                   after_sleep=0.5),
                           raise_if_not_found=False):
            self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
            self.count += 1
            self.trigger_count += 1
            return True
        else:
            self.log_warning("没有检测到战斗结束")
            return False

        