import re
import random

from src.tasks.BaseOmjTask import BaseOmjTask


class BaseBattleTask(BaseOmjTask):
    """战斗任务基类：统一管理阵容锁定、预设队伍切换等战斗配置。"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.green = {
            1: (0.1, 0.75),
            2: (0.3, 0.67),
            3: (0.45, 0.62),
            4: (0.61, 0.71),
            5: (0.79, 0.75),
            6: (0.44, 0.85),
        }
        self.group = 0
        self.team = 0

        self.trigger_count = 1 #想法是 多次启动多次记录
        self.count = 1 #每次启动战斗的次数 每次启动刷新的


        self.next_sleep_count = 0
        self.is_sleep = 0
        self.count_range = [0,0]
        self.time_range = [0,0]

        self.default_config.update({
            "RandomSleep":"1,3,10,30,60",
            "Lock Team Enable": True,
            "Preset Enable": False,
            "Preset Team": "1,1",
            "Team Name":"",
            "AttackNumber":"1",
            "BattleTime": "180",
            "Green Enable": "0",
        })

        self.config_description.update({
            "RandomSleep": "以1,3,10,30,60为例，1表示开启0关闭，3，10为在这个范围随机次数打多少次会休息，30，60为随机休息多少秒，建议大量的战斗都开启这个功能，模拟人操作",
            "Lock Team Enable": "不开启时默认锁定阵容，开启后第一次将切换阵容第二次锁定",
            "Preset Enable": "开启后战斗前自动切换到指定的预设队伍。",
            "Preset Team": "预设队伍编号，格式：组,队  例如 1,5 表示第1组第4个队伍，最大支持7和4。和Team Name二选一填写",
            "Team Name": "此功能暂时没设置好不要使用，预设组，队伍名，理论上可以让队伍选择更多，但是推荐尽量用上面那个，因为更稳定",
            "BattleTime": "通过时间 一般情况下不用修改",
            "Green Enable": "是否绿标，从左到右填写1-6，6为阴阳师，0为不绿标"
        })
        self.config_type.update({
        })

    @property
    def AttackNumber(self):
        return int(self.config["AttackNumber"])

    @property
    def BattleTime(self):
        return int(self.config["BattleTime"])

    @property
    def GreenNum(self):
        return int(self.config["Green Enable"])

    def _parse_preset(self, preset="1,1"):
        """解析 组,队 字符串（如 "1,5"），返回 (group, team)。"""
        parts = preset.split(",")
        if len(parts) == 2:
            return int(parts[0].strip()), int(parts[1].strip())
        return 1, 1
    def _random_sleep(self,randomsleep):
        parts = randomsleep.split(",")
        if len(parts) == 5:
            return (int(parts[0].strip()),[int(parts[1].strip()), int(parts[2].strip())],
                    [int(parts[3].strip()), int(parts[4].strip())])
        return 0,[0,0],[0,0]

    def _rect_random_point(self, rect, margin=0.1):
        """在矩形内取随机点（默认中间 80% 区域）。支持相对坐标元组 (x1,y1,x2,y2) 或 Box 对象。"""
        if hasattr(rect, 'x'):  # Box 对象，转相对坐标
            h, w = self.frame.shape[:2]
            rect = (rect.x / w, rect.y / h, (rect.x + rect.width) / w, (rect.y + rect.height) / h)
        x1, y1, x2, y2 = rect
        x = random.uniform(x1 + (x2 - x1) * margin, x2 - (x2 - x1) * margin)
        y = random.uniform(y1 + (y2 - y1) * margin, y2 - (y2 - y1) * margin)
        return x, y

    def click_rect_random(self, rect, margin=0.1, after_sleep=1):
        """在矩形内随机点击。"""
        x, y = self._rect_random_point(rect, margin)
        self.click_relative(x, y, after_sleep=after_sleep)
        self.log_info(f"点击{x:.2f},{y:.2f}")

    def SwitchSoul_by_name(self,group:int,team:int,team_name:str):
        if self.wait_click_feature('Home_Shikigami_Chronicles', threshold=0.7,
                                   box=self.B('bottom'),
                                   raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("Home_Shikigami_Chronicles")
            self.info_set("步骤", "进入Home_Shikigami_Chronicles")
        elif text := self.ocr_and_click(['式神'], 1, box=self.B('Home_Shikigami_Chronicles')):
            self.log_info(f"OCR: {text}")
        else:
            self.log_info('找不到Home_Shikigami_Chronicles')
            return False

        if self.wait_click_ocr(match='预设',
                               box=self.B('Home_Shikigami_Presets'), time_out=6, after_sleep=1):
            self._swipe(0.91, 0.22, 0.91, 0.77, 0.5)
            self.sleep(0.5)

        group_rows = {1: 0.17, 2: 0.27, 3: 0.35, 4: 0.47, 5: 0.56, 6: 0.67, 7: 0.75}
        self.click_nth('x', 0.91, group_rows, group, "预设组")

        self._swipe(0.59, 0.19, 0.59, 0.81, 0.2)  # 从第一个开始
        self._swipe(0.59, 0.19, 0.59, 0.81, 0.2)  # 从第一个开始
        for i in range(2):
            self._swipe(0.59, 0.81, 0.59, 0.19, 1)  # 从第一个开始
            if res := self.ocr(match=re.compile(self.config["Team_Name"]),
                               box=self.box_of_screen(0.4, 0.18, 0.65, 0.9)):
                # 只有一个关键词，取第一个匹配结果，算 y 中心，从右列点击
                h = self.frame.shape[0]
                match = res[0]
                center_y = (match.y + match.height / 2) / h
                self.click_relative(0.77, center_y)
                self.sleep(0.5)
                if text := self.ocr('确认', box=self.box_of_screen(0.50, 0.53, 0.66, 0.63)):
                    self.click(text[0], after_sleep=0.5)
                if text := self.ocr('确认', box=self.box_of_screen(0.50, 0.53, 0.66, 0.63)):
                    self.click(text[0], after_sleep=0.5)
                break
            elif i == 1:
                self.log_warning("换御魂失败")
                return  False
        if not self.wait_click_feature('Back', threshold=0.7,
                                       box=self.B('Back'),
                                       raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info('回家')
            return True
        else:
            self.log_info('找不到Home_Shikigami_Chronicles')
            self.in_home_and_back()

    def SwitchSoul_by_num(self,group:int,team:int):
        """按编号切换预设队伍（从 config 读取 Preset Group / Preset Team)。"""

        if self.wait_click_feature('Home_Shikigami_Chronicles', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("Home_Shikigami_Chronicles")
            self.info_set("步骤", "进入Home_Shikigami_Chronicles")
        elif text:=self.ocr_and_click(['式神'],1,box=self.B('Home_Shikigami_Chronicles')):
            self.log_info(f"OCR: {text}")
        else:
            self.log_info('找不到Home_Shikigami_Chronicles')
            return False
    

        if self.wait_click_ocr(match='预设',
                            box=self.B('Home_Shikigami_Presets'),time_out=6,after_sleep=1):
            self._swipe(0.91,0.22,0.91,0.77,0.5)
            self.sleep(0.5)

            group_rows = {1: 0.17, 2: 0.27, 3: 0.35, 4: 0.47, 5: 0.56, 6: 0.67, 7: 0.75}
            self.click_nth('x', 0.91, group_rows, group, "预设组")

            team_rows = {1: 0.22, 2: 0.44, 3: 0.64, 4: 0.85}
            self.click_nth('x', 0.77, team_rows, team, "预设队伍")

            self.sleep(1)
            if text := self.ocr('确认',box=self.box_of_screen(0.50,0.53,0.66,0.63)):
                self.click(text[0],after_sleep=0.5)
            if text := self.ocr('确认',box=self.box_of_screen(0.50,0.53,0.66,0.63)):
                self.click(text[0],after_sleep=0.5)
            if self.wait_click_feature('Back', threshold=0.7,
                                            box=self.B('Back'),
                                            raise_if_not_found=False, time_out=6, after_sleep=1):
            
                self.log_info('回家')
            else:
                self.log_info('找不到Home_Shikigami_Chronicles')
        self.in_home_and_back()



    def _invite_tabs(self, base_tabs=None, first=None):
        """返回按优先搜索重排后的标签页列表。"""
        if base_tabs is None:
            base_tabs = ["最近", "好友", "跨区", "寮友"]
        tabs = list(base_tabs)
        if first is None:
            first = tabs[0]
        if first in tabs:
            tabs.remove(first)
            tabs.insert(0, first)
        return tabs
# region 预设
    def Lock_team(self, confirm_box: tuple,lock = True):
        LOCK_NAMES = ["Soul_Lock", "Lock", "Areaboss_Lock", "RealmRaid_Lock","Secret_Lock"]
        NOT_LOCK_NAMES = ["Soul_Not_Lock", "Not_Lock", "Areaboss_Not_Lock", "RealmRaid_Not_Lock","Secret_Not_Lock"]
        if res := self.find_one(LOCK_NAMES, threshold=0.85, box=self.box_of_screen(*confirm_box)):
            self.log_info("检查到上锁")
            if lock:
                self.log_info("上锁")
                return True
            else:
                self.click(res)
                self.log_info("解锁")
                return False
        elif res := self.find_one(NOT_LOCK_NAMES, threshold=0.85, box=self.box_of_screen(*confirm_box)):
            if lock:
                self.click(res)
                self.log_info("上锁")
                return True
            else:
                self.log_info("解锁")
                return False
    def Change_team(self,group:int,team:int):
        self.log_info("进入检测2")
        if self.wait_click_ocr(match=re.compile("预设"),
                            box=self.box_of_screen(0.02, 0.87, 0.14, 1.0),
                            raise_if_not_found=False, time_out=120):
            self.sleep(2)
            group_rows = {1: 0.36, 2: 0.45, 3: 0.54, 4: 0.63, 5: 0.72, 6: 0.81, 7: 0.90}
            self.click_nth('x', 0.08, group_rows, group, "预设组")
            self.sleep(0.5)

            team_rows = {1: 0.36, 2: 0.53, 3: 0.69, 4: 0.85}
            self.click_nth('x', 0.35, team_rows, team, "预设队伍")
            self.sleep(0.5)
            if self.wait_click_ocr(match=re.compile("确定"),
                                   box=self.box_of_screen(0.26, 0.88, 0.40, 0.96),
                                   raise_if_not_found=False, time_out=2):
                self.click_relative(0.33, 0.93, after_sleep=0.5)
                self.log_warning("御魂不一致！！")
                #开战
                self.click_relative(0.91, 0.79)
                return True
            else:
                # 开战
                self.click_relative(0.33,0.93,after_sleep=0.5)
                self.click_relative(0.91, 0.79)
                return True
        else:
            self.click_relative(0.91, 0.79)
            self.log_warning("没有识别到预设")
            return False
# endregion
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

        if self.wait_until(check, time_out=battle_time, raise_if_not_found=False):
            return result

        self.log_warning("战斗结束超时")
        return 3
    def open_buff(self, selected):
        """根据 selected（buff 名列表），先 OCR 定位加成文字位置，再检查/点击对应开关。
        不同用户加成数量不同，OCR 自适应。"""
        if not selected:
            return True
        if not self.ocr_and_click('成',box=self.box_of_screen(0.31, 0.03, 0.35, 0.11)):
            self.log_info("不在探索页面，跳过加成")
            return False

        # 1. OCR 定位屏幕上实际存在的加成文字
        buff_pattern = '|'.join(selected)
        results = self.ocr(
            match=re.compile(buff_pattern),
            box=self.box_of_screen(0.29, 0.18, 0.72, 0.68),
        )
        if not results:
            self.log_info("OCR 未检测到任何加成文字")
            return True

        h = self.frame.shape[0]

        for name in selected:
            # 找到这个 buff 的 OCR 结果
            match = next((r for r in results if name in r.name), None)
            if match is None:
                self.log_info(f"屏幕上未找到加成文字: {name}")
                continue

            # 2. 从 OCR y 坐标推算开关盒子位置（x 固定 0.67~0.69，y 与文字对齐）
            rel_y_top = match.y / h
            rel_y_bot = (match.y + match.height) / h
            toggle_box = self.box_of_screen(0.67, rel_y_top, 0.69, rel_y_bot)

            # 3. 颜色检测：ON=rgb(243,238,193)→BGR(193,238,243) / OFF=rgb(158,155,126)→BGR(126,155,158)
            on_ratio = self.calculate_color_percentage(
                {"b": (180, 210), "g": (230, 250), "r": (235, 255)},
                box=toggle_box,
            )
            if on_ratio > 0.2:
                self.log_info(f"{name} 加成已开启")
            else:
                self.log_info(f"{name} 加成未开启，点击打开")
                self.click_relative(0.68, (rel_y_top + rel_y_bot) / 2, after_sleep=0.5)
        self.sleep(1)
        self.click_relative(0.32,0.07)
        return True

    def change_auto(self,GreenNum=0):
        def check():
            if self.wait_ocr(
                    match=re.compile('妖术|普攻|自动'),
                    box=self.box_of_screen(0.02, 0.85, 0.99, 1.0),
                    time_out=1
            ):
                self.log_info("自动")
                self.sleep(0.3)
                if GreenNum != 0:
                    x, y = self.green[GreenNum]
                    self.click_relative(x, y, after_sleep=1)
                    return True
                return True
            elif res := self.ocr( match=re.compile('手动'),
                                  box=self.box_of_screen(0.02, 0.88, 0.08, 0.96)):
                self.click(res[0])
                self.sleep(0.3)
                self.log_info("点击 切换自动")
                if GreenNum != 0:
                    x, y = self.green[GreenNum]
                    self.click_relative(x, y, after_sleep=1)
                return False
            return False
        if self.wait_until(check, time_out=5, raise_if_not_found=False):
            return True
    def click_green(self,GreenNum):
        self.log_info("进入绿标")
        if GreenNum != 0:
            self.log_info("进入绿标2")
            self.log_info(GreenNum)
            if self.wait_ocr(
                    match=re.compile('妖术|普攻|自动'),
                    box=self.box_of_screen(0.02, 0.85, 0.99, 1.0),
                    time_out=8
            ):
                self.sleep(0.3)
                x, y = self.green[GreenNum]
                self.log_info(x,y)
                self.click_relative(x, y, after_sleep=1)
                return True
        return False
