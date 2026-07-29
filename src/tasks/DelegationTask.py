import re

from src.tasks.BaseOmjTask import BaseOmjTask


class DelegationTask(BaseOmjTask):

    # 配置项 → 游戏内中文翻译
    DELEGATION_MAP = {
        "Bird Feather": "鸟之羽",
        "Find Earring": "寻找|耳环",
        "Cat Boss": "猫|老大",
        "Miyoshino": "接|送弥助",
        "Strange Trace": "奇怪的|痕迹",
        "Miyoshino Painting": "弥助的|画",
        "Fish":"以鱼|为礼"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-式神委派"
        self.default_config.update({
            "Bird Feather": False,
            "Find Earring": False,
            "Cat Boss": False,
            "Miyoshino": False,
            "Strange Trace": False,
            "Miyoshino Painting": False,
            "Fish":False ,
        })
        self.config_description.update({
            "Bird Feather": "50体力->20片大蛇的逆鳞",
            "Find Earring": "300体力->金币28万",
            "Cat Boss": "300体力->四星白蛋",
            "Miyoshino": "100体力->三星结界卡",
            "Miyoshino Painting": "300体力->六星变异卡",
            "Strange Trace": "100体力->金币九万八",
            "Fish":"四星结界卡" ,
        })

    def run(self):
        self.in_home_and_back()
        if not self.Delegation_page():
            self.log_warning("Delegation_page 失败")
            return False
        if not self.Finish_delegation():
            self.log_warning("Finish_delegation 失败")
            return False
        if not self.Delegation_selet():
            self.log_warning("Delegation_selet 失败")
            return False
        if self.wait_click_feature('Home_Button', box=self.B('Home_Button'), time_out=3,threshold=0.8):
            self.log_info('点击 Home_Button')
        if not self.in_home_and_back():
            self.log_warning("Back_Home 失败")
            return False
        return True


    def Delegation_page(self):
        """导航到式神委派页面"""
        self.log_info('导航')

        if not self.wait_click_feature('Home_Explore', threshold=0.7,
                                        box=self.B('Home_Explore'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_warning("找不到探索 Home_Sign")
        self.info_set("步骤", "进入探索页面")
        if self.wait_click_feature('Exploration_Delegation', threshold=0.7,
                                        box=self.B('bottom'),
                                        raise_if_not_found=False, time_out=6, after_sleep=1):
            self.log_info("探索 Delegation")
            self.info_set("步骤", "进入Delegation")
            return True
        else:
            if text:=self.ocr_and_click(['式神', '委派'],1,box=self.box_of_screen(0.3293, 0.8708, 0.407, 0.9833)):
                return True
            else:
                self.log_info('找不到式神委派')
                return False
    def Delegation_selet(self):
        """根据用户配置，在委派列表中识别并点击已启用的委派任务。"""
        self.log_info('进入委派任务')
        self._swipe(0.85, 0.80, 0.85, 0.30, 0.5)
        self.sleep(1)

        # 收集已启用任务的翻译名
        enabled = [(k, t) for k, t in self.DELEGATION_MAP.items() if self.config.get(k, False)]
        if not enabled:
            self.log_info('没有启用的委派任务')
            return True

        # 正则一键匹配（括号分组，防止不同任务的|互相干扰）
        pattern = '|'.join(f"({t})" for _, t in enabled)
        results = self.ocr(match=re.compile(pattern), box=self.B("Delegation"))
        if not results:
            self.log_info('检测到 0 个可见任务')
            return True

        self.log_info(f"检测到 {len(results)} 个可见任务: {[r.name for r in results]}")

        for r in results:
            translation = r.name
            if not self.ocr_and_click(translation, 1, box=self.B("Delegation")):
                self.log_info(f'找不到委派任务: {translation}')
            else:
                self.info_set("委派", f"已点击 {translation}")
                if self.wait_ocr(match=re.compile("召回"), box=self.box_of_screen(0.73, 0.35, 0.93, 0.53),
                                 threshold=0.8, time_out=3, raise_if_not_found=False):
                    self.log_info('找到还未完成的任务')
                    if self.wait_click_ocr(match=re.compile("返回"),
                                        time_out=3,
                                        box=self.box_of_screen(0.73, 0.35, 0.93, 0.7)):
                        self.log_info("返回")
                    else:
                        self.click_relative(0.78,0.62)
                elif self.wait_click_ocr(match=re.compile("跳过"),
                                        time_out=3,
                                        box=self.box_of_screen(0.5, 0.7, 0.61, 0.79)):
                    self.Delegation()
                    self._swipe(0.85, 0.80, 0.85, 0.30, 0.5)
                elif self.Delegation():
                        self.log_info("没有跳过")
                else:
                    return False
        return True

    def Finish_delegation(self):
        if self.wait_ocr(match=re.compile("式神|委派"),
                         box=self.box_of_screen(0, 0, 0.17, 0.1), time_out=6):
            self.log_info("回到式神委派页面")
        self.log_info('检查是否有已完成的委派')
        self._swipe(0.85, 0.80, 0.85, 0.30, 0.5)
        self.sleep(1)
        while (self.ocr(match=re.compile("完成"),
                                        box=self.B("Delegation"))):
            self.sleep(0.5)
            self.click_relative(0.93, 0.27)
            # self.click_relative(0.89, 0.44, after_sleep=1) ？？？
            self.wait_until(condition=lambda: self.ocr_and_click(['完成'], 1, time_out=0.5,
                                            box=self.box_of_screen(0.73, 0.35, 0.93, 0.53)),
                                            time_out=20, post_action=lambda: self.click_relative(0.47, 0.81, after_sleep=0.5)
                                            , raise_if_not_found=False)

            if not self.ocr_and_click(['顺利', "达成"], 1,
                                        box=self.box_of_screen(0.26, 0.05, 0.8, 0.29), raise_if_not_found=False):
                self.log_warning("找不到Battle_Success_Soul")
            self.sleep(2)
        self.log_info('没有待完成')
        return True

    def Delegation(self):
        if not self.wait_click_ocr(match=re.compile("委派|式神"),
                               time_out=3,
                               box=self.box_of_screen(0.73, 0.35, 0.93, 0.53),):
            self.log_warning('找不到式神委派')
        if not self.wait_click_ocr(match=re.compile("一键|选择"),
                               time_out=3,
                               box=self.box_of_screen(0.85, 0.59, 0.98, 0.88),):
            self.log_warning('找不到一键')
        if self.wait_click_ocr(match=re.compile("出发"),
                               time_out=3,
                               box=self.box_of_screen(0.85, 0.59, 0.98, 0.88),):
            self.log_warning('找到出发')
            if self.wait_ocr(match=re.compile("式神|委派"),
                                    box=self.box_of_screen(0, 0, 0.17, 0.1), time_out=6):
                self.log_info("回到式神委派页面")
                return True
        else:
            return False
