from ok import communicate

from src.tasks.BaseBattleTask import BaseBattleTask


class WantedQuestsTask(BaseBattleTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-悬赏封印"
        self.description = "自动完成悬赏封印，不会完成勾协，但会提示有勾协，勾协请手动完成"
    def run(self):
        self.in_home_and_back()
        self.wanted_page()
        if not self.wanted_battle():
            self.log_warning("悬赏失败")
    def wanted_page(self):

        if btns := self.find_feature('Wanted',
                                     box=self.box_of_screen(0.16, 0.17, 0.27, 0.6), threshold=0.8):
            self.click_rect_random(btns[0])
            self.log_info('点击悬赏封印')
        self.sleep(1)
        if btns := self.find_feature('Wanted2',
                                     box=self.box_of_screen(0.16, 0.17, 0.27, 0.6), threshold=0.8):
            self.click_rect_random(btns[0])
            self.log_info('点击悬赏封印')
        self.sleep(1)

        if not self.wait_feature('WantedQuests_Feature', threshold=0.7,
                                 box=self.box_of_screen(0.42, 0.05, 0.59, 0.18),
                                 raise_if_not_found=False, time_out=3):
            self.log_warning("找不到悬赏封印")
            return False
        self.log_info("进入悬赏")
    def wanted_battle(self):
        a= (0.11, 0.23, 0.32, 0.83)
        click_rows={
            1: (0.11, 0.56, 0.32, 0.7),
            2: (0.34, 0.56, 0.56, 0.7),
            3: (0.58, 0.56, 0.79, 0.7),
            4: (0.81, 0.56, 0.9, 0.7),
        }
        click_rows2 = {
            1: (0.2, 0.52, 0.24, 0.57),
            2: (0.66, 0.53, 0.7, 0.57),
            3: (0.43, 0.52, 0.47, 0.58),
        }
        self.count = 1 #打到第几个了
        self.trigger_count = 1 #战斗了几次

        while self.count <= 4:

            if self.count == 1:
                jade = self.find_one(["Home_WantedQuests_Jade"],
                                     threshold=0.75, box=self.box_of_screen(0.11, 0.23, 0.32, 0.83))
                self.sleep(0.5)
                friend = self.find_one(["Home_WantedQuests_Friend","Home_WantedQuests_Friend2"],
                                       threshold=0.75, box=self.box_of_screen(0.11, 0.23, 0.32, 0.83))
                if jade and friend:
                    communicate.notification.emit('有勾协请手动处理', '提示', False, True, None, None)
                    self.log_warning("有勾协请手动处理")
                    self.count += 1
                    continue
                if friend:
                    self.count += 1
                    self.log_warning("有需要邀请好友的任务请手动处理")

                    continue
            self.click_rect_random(click_rows[self.count])
            self.log_info(f"开始{self.count}个悬赏")
            if self.wait_feature('Wanted_Todo_Feature', threshold=0.7,
                                       box=self.box_of_screen(0.39, 0.28, 0.54, 0.44),
                                       raise_if_not_found=False, time_out=3):
                self.sleep(0.5)
                self.log_info("式神碎片挑战")
                self.click_rect_random((0.77, 0.35, 0.83, 0.4))
            else:
                self.log_info("不是式神碎片挑战或者已经完成，跳过，")
                self.click_rect_random((0.09, 0.09, 0.87, 0.17))
                self.sleep(1)
                self.count += 1
                continue
            if self.wait_feature('Shikigami_Challenge', threshold=0.7,
                                 box=self.box_of_screen(0.37, 0.0, 0.42, 0.09),
                                 raise_if_not_found=False, time_out=3):
                self.log_info("进入式神碎片挑战页面")
                if self.config["Lock Team Enable"]:
                    # 解锁状态 准备换队伍

                    self.Lock_team((0.83, 0.6, 0.93, 0.78), lock=False)
                else:
                    # 不换
                    self.Lock_team((0.83, 0.6, 0.93, 0.78), lock=True)
                self.click_rect_random((0.85, 0.82, 0.92, 0.92)) #开始战斗

                if self.trigger_count == 1:
                    self.log_info("进入检测1")
                    if self.config["Lock Team Enable"]:
                        self.Change_team(self.group, self.team)

                    self.log_info("检测是否为自动")
                    self.change_auto(self.green,self.GreenNum)
                else:
                    self.click_green(self.green,self.GreenNum)
                res = self.Find_finish(self.BattleTime)
                if res == 2:
                    self.log_warning("战斗失败！！")
                    return False
                elif res == 3:
                    self.log_warning("战斗超时！！")
                    return False
                self.trigger_count += 1
                self.count += 1
                if not self.wait_click_feature('Home_Button', box=self.B('Home_Button'), threshold=0.8,
                                               raise_if_not_found=False,
                                               time_out=6):
                    self.log_warning("找不到返回")
                    return False
                if self.count !=4:
                    if self.In_Home():
                        self.sleep(1)
                        if btns := self.find_feature('Wanted',
                                                     box=self.box_of_screen(0.16, 0.17, 0.27, 0.6), threshold=0.8):
                            self.click_rect_random(btns[0])
                            self.log_info('点击悬赏封印')
                            self.sleep(1)
                        elif btns := self.find_feature('Wanted2',
                                                     box=self.box_of_screen(0.16, 0.17, 0.27, 0.6), threshold=0.8):
                            self.click_rect_random(btns[0])
                            self.log_info('点击悬赏封印')
                        self.sleep(1)
                    if not self.wait_feature('WantedQuests_Feature', threshold=0.7,
                                             box=self.box_of_screen(0.42, 0.05, 0.59, 0.18),
                                             raise_if_not_found=False, time_out=3):
                        self.log_warning("找不到悬赏封印")
                        return False
                    self.log_info("进入悬赏")
                    self.sleep(0.5)
                    self.click_rect_random(click_rows2[self.count])
                    self.log_info("点击领取")
                    self.sleep(1)
                    self.click_rect_random((0.09, 0.09, 0.87, 0.17))
        return True







