import re

from src.tasks.BaseBattleTask import BaseBattleTask


class AreaBossTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-战斗-地域鬼王"

        self.default_config.update({
            "Area Boss": "悬赏",
        })
        self.config_description.update({
            "RandomSleep": "对于鬼王来说这个功能没什么用将参数改为0,0,0,0,0即可",
            "Area Boss": "打谁，强烈建议打收藏",
            "Lock Team Enable": "地域鬼王很特殊，为了避免出现打鬼王限定式神建议不要勾选此项，锁定阵容打1级自动战斗即可",
        })
        self.config_type.update({
            "Area Boss": {
                "type": "drop_down",
                "options": ["悬赏", "热门", "最新", "征服", "收藏"],
            },
        })


    def run(self):

        self.in_home_and_back()
        self.group, self.team = self._parse_preset(self.config["Preset Team"])
        if self.config["Preset Enable"]:
            self.SwitchSoul_by_num(self.group, self.team)
        if not self.AreaBoss_page():
            self.log_warning("找不到鬼王页面")
            return False
        if not self.Battle():
            self.log_warning("battle失败")
            return False
        self.sleep(1)
        self.Back_Home()
        return True

    def AreaBoss_page(self):
        # self.In_Home()
        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        if self.wait_click_feature('Exploration_AreaBoss', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("探索 AreaBoss")
            self.info_set("步骤", "进入探索页面")
            return True
        else:
            if text:=self.ocr_and_click(['地域','鬼王'],1,box=self.box_of_screen(0.48,0.94,0.55,0.98)):
                self.log_info(f"OCR: {text}")
                return True
            else:
                return False
        

    def Battle(self):
        self.log_info("进入battle")
        self.count = 1
        while(self.count <= self.AttackNumber):
            if not (text := self.ocr_and_click(['收', '藏'],0.5, time_out=2, box=self.B('Areaboss_Filter_Page'))):
                self.log_info(f"OCR: {text}")
                if self.wait_click_feature('Areaboss_Filter', threshold=0.7,
                                            box=self.B('Areaboss_Filter'),
                                            raise_if_not_found=False, time_out=5, after_sleep=1):
                    self.log_info("探索 AreaBoss")
                    self.info_set("步骤", "进入探索页面")
                elif text:=self.ocr_and_click(['筛','选'],time_out=5,box=self.B('Areaboss_Filter')):
                    self.log_info(f"OCR: {text}")
                self.wait_click_ocr(match=re.compile(self.config["Area Boss"]),
                                    box=self.B('Areaboss_Filter_Page'),
                                    time_out=3)
            self.sleep(1)
            group_rows = {
                1: (0.84, 0.32, 0.9, 0.42),
                2: (0.84, 0.53, 0.9, 0.63),
                3: (0.84, 0.75, 0.9, 0.84),
            }
            self.click_rect_random(group_rows[self.trigger_count])
            if self.config["Lock Team Enable"]:#地域鬼王的锁定是放在循环内部的
                # 解锁状态 准备换队伍
                self.Lock_team((0.86,0.88,1,1), lock=False)
            else:
                # 不换
                self.Lock_team((0.86,0.88,1,1), lock=True)
             

            if text:=self.ocr_and_click(['挑战'],0.5,box=self.box_of_screen(0.86,0.73,0.93,0.79)):
                self.log_info(f"OCR: {text}")
            if self.config["Lock Team Enable"]:
                self.Change_team(self.group, self.team)
            self.log_info("检测是否为自动")
            self.change_auto(self.green,self.GreenNum)

            self.click_green(self.green,self.GreenNum)
            res = self.Find_finish(self.BattleTime)
            if res == 2:
                self.log_warning("战斗失败！！")
                return False
            elif res == 3:
                self.log_warning("战斗超时！！")
                return False
            
            if not self.wait_click_feature('Daily_New_Cancel', threshold=0.7,
                                    box=self.B('Daily_New_Cancel'),
                                    raise_if_not_found=False, time_out=5, after_sleep=1):
                self.log_warning("找不到Daily_New_Cancel")
                self.Back_Home()
                return False
            self.log_info(f"第 {self.count} 次战斗结束 总共{self.AttackNumber} 第 {self.trigger_count} 次战斗")
            self.count+=1
            self.trigger_count+=1
        return True

    def Battle_process(self):
        pass

        
        
        