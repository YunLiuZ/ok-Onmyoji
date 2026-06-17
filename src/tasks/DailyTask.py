from ok import og
from src.tasks.MyBaseTask import MyBaseTask
from src.tasks.BaseOmjTask import BaseOmjTask


class DailyTask(BaseOmjTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "每日签到"
        self.description = "签到加黑碎"

    def run(self):
        self.Sign()
        self.Gift_Shop_Sign()

    def Sign(self):
        """签到流程

        1. 确认在主页
        2. 点击签到入口 Home_Sign
        3. 点击一键完成 Sign_Button
        4. 分支判断：
           - 分支A: 检测到 Sign_Daily_Skip → 点击跳过 →
                    Daily_New_Cancel → Daily_Sign_Success → Home_Button
           - 分支B: 直接检测到 Daily_Sign_Success → Home_Button
        """
        # 1. 确认在主页，不在主页则跳过
        if not self.In_Home():
            self.log_info("不在主页")
            if self.Back_Home() is not True:
                return
        # 2. 等待签到入口出现并点击
        if not self.wait_click_feature('Home_Sign', threshold=0.6,box=self.box_of_screen(0.4, 0.5, 0.7, 0.7),
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到签到入口 Home_Sign")
            self.click_relative(0.64,0.6)
        self.info_set("步骤", "进入签到页面")
        # 3. 等待一键完成按钮出现并点击
        if not self.wait_click_feature('Sign_Button', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到一键完成 Sign_Button")
            return
        self.info_set("步骤", "已点击一键完成")

        # 4. 判断分支：先检测 Sign_Daily_Skip
        skip = self.wait_feature('Sign_Daily_Skip', threshold=0.6,
                                  raise_if_not_found=False, time_out=2)
        if skip:
            # 分支A：需要跳过每日签到动画
            self.click_box(skip, after_sleep=0.5)
            self.info_set("步骤", "跳过每日签到")

            # 等待 Daily_New_Cancel 出现并点击
            if not self.wait_click_feature('Daily_New_Cancel', threshold=0.6,
                                            raise_if_not_found=False, time_out=3):
                self.log_warning("找不到 Daily_New_Cancel")
                return

            # 等待签到成功出现并点击
            if not self.wait_click_feature('Daily_Sign_Success', threshold=0.6,
                                            raise_if_not_found=False, time_out=3):
                self.log_warning("找不到签到成功 Daily_Sign_Success")
                return

            # 返回主页
            if not self.wait_click_feature('Home_Button', threshold=0.6,
                                            raise_if_not_found=False, time_out=5):
                self.log_warning("找不到主页按钮 Home_Button")
                return
        else:
            # 分支B：直接检测到签到成功
            if not self.wait_click_feature('Daily_Sign_Success', threshold=0.6,
                                            raise_if_not_found=False, time_out=3):
                self.log_warning("找不到签到成功 Daily_Sign_Success")
                return

            # 返回主页
            if not self.wait_click_feature('Home_Button', threshold=0.6,
                                            raise_if_not_found=False, time_out=5):
                self.log_warning("找不到主页按钮 Home_Button")
                return

        self.log_info("签到完成 ✅", notify=True)

    def Gift_Shop_Sign(self):
        """礼包屋签到流程

        1. 确认在主页
        2. Home_Store → Gift_Store → Gift_Daily → Gift_Daily_Fnish → Gift_Fnish → Home_Button
        """
        # 1. 确认在主页，不在主页则跳过
        if not self.In_Home():
            self.log_warning("不在主页，跳过礼包屋签到")
            return

        # 2. 等待商店入口出现并点击
        if not self.wait_click_feature('Home_Store', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到商店入口 Home_Store")
            return
        self.info_set("步骤", "进入商店")

        # 3. 等待礼包商店出现并点击
        if not self.wait_click_feature('Gift_Store', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到礼包商店 Gift_Store")
            return
        self.info_set("步骤", "进入礼包商店")

        # 4. 等待每日礼包出现并点击
        if not self.wait_click_feature('Gift_Daily', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到每日礼包 Gift_Daily")
            return
        self.info_set("步骤", "进入每日礼包")

        # 5. 等待每日礼包完成出现并点击
        if not self.wait_click_feature('Gift_Daily_Finish', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到每日礼包完成 Gift_Daily_Fnish")
            return
        self.info_set("步骤", "每日礼包完成")

        # 6. 等待礼包完成出现并点击
        if not self.wait_click_feature('Gift_Finish', threshold=0.6,
                                        raise_if_not_found=False, time_out=3):
            self.log_warning("找不到礼包完成 Gift_Fnish")
            return
        self.info_set("步骤", "礼包完成")

        # 7. 返回主页
        if not self.wait_click_feature('Home_Button', threshold=0.6,
                                        raise_if_not_found=False, time_out=5):
            self.log_warning("找不到主页按钮 Home_Button")
            return

        self.log_info("礼包屋签到完成 ✅", notify=True)

    # ---------- 测试辅助方法 ----------

    def find_home_sign(self):
        """测试用：在当前帧中匹配 Home_Sign 模板"""
        return self.find_one('Home_Sign', threshold=0.6)
