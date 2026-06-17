import math
import re
import time
from datetime import datetime, timedelta
from typing import List

import numpy as np

from ok import BaseTask, Logger, find_boxes_by_name, og, find_color_rectangles, mask_white
from ok import CannotFindException
import cv2

from ok import BaseTask

class BaseOmjTask(BaseTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "基本设置"
        self.description = "切换御魂 判断是否在主页"
    # 不太确定logged_in(self):    @logged_in.setter
    @property 
    def logged_in(self):
        return og.my_app.logged_in

    @logged_in.setter
    def logged_in(self, value):
        og.my_app.logged_in = value


    def In_Home(self):
        return self.find_one(
            ['Home_Town', 'Home_Store', 'Home_Sign'],
            threshold=0.6
        ) is not None


    def Back_Home(self):
        self.log_info('进入backhome')
        if self.In_Home():
            return True
        search_box = self.box_of_screen(
            0, 0,       # 左上角
            0.2, 0.2    # 右下角
        )
        def try_back():
            if home_button:= self.find_one(
                'Home_Button',
                box=search_box,
                threshold=0.6
            ):
                self.click(home_button, after_sleep=3)
                self.log_info('点击Home_Button')
                return


            if back_button:= self.find_one(
                'Back',
                box=search_box,
                threshold=0.6
            ):
                self.click(back_button, after_sleep=3)
                self.log_info('点击Back')
                return
            
            if Back := self.find_one(['Cancel_Old','Daily_New_Cancel'],box=self.box_of_screen(0.7,0,1,0.7),threshold=0.5):
                self.click(Back, after_sleep=2)
                self.log_info('关闭了某个窗口!')
                return
            self.log_info('什么都没点击')
            self.click_relative(0.1,0.05,after_sleep=3)

        return self.wait_until(
            self.In_Home,
            time_out=20,
            post_action=try_back,
            raise_if_not_found=False
        )