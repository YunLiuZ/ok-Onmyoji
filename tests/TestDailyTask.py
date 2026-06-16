"""DailyTask 模板匹配测试"""
import unittest

from src.config import config
from ok.test.TaskTestCase import TaskTestCase
from src.tasks.DailyTask import DailyTask


class TestDailyTask(TaskTestCase):
    task_class = DailyTask
    config = config

    TEST_IMAGE = 'tests/images/ADB command line Capture_2560x1440_1781624038781.4026_original.png'

    def test_home_sign_match_default_threshold(self):
        """默认阈值 0.8 下匹配 Home_Sign"""
        self.set_image(self.TEST_IMAGE)
        feature = self.task.find_one('Home_Sign')
        if feature:
            print(f"Home_Sign found at default threshold 0.8: "
                  f"x={feature.x}, y={feature.y}, "
                  f"w={feature.width}, h={feature.height}, "
                  f"confidence={feature.confidence:.3f}")
        self.assertIsNotNone(feature, "默认阈值 0.8 下未找到 Home_Sign")

    def test_home_sign_match_threshold_06(self):
        """阈值 0.6 下匹配 Home_Sign"""
        self.set_image(self.TEST_IMAGE)
        feature = self.task.find_one('Home_Sign', threshold=0.6)
        if feature:
            print(f"Home_Sign found at threshold 0.6: "
                  f"x={feature.x}, y={feature.y}, "
                  f"w={feature.width}, h={feature.height}, "
                  f"confidence={feature.confidence:.3f}")
        self.assertIsNotNone(feature, "阈值 0.6 下未找到 Home_Sign")

    def test_home_sign_threshold_sweep(self):
        """遍历不同阈值，看 Home_Sign 在哪个阈值开始匹配不到"""
        self.set_image(self.TEST_IMAGE)
        for threshold in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4]:
            feature = self.task.find_one('Home_Sign', threshold=threshold)
            status = "HIT " if feature else "MISS"
            conf = f"confidence={feature.confidence:.3f}" if feature else "confidence=N/A"
            print(f"  threshold={threshold} -> {status} ({conf})")


if __name__ == '__main__':
    unittest.main()
