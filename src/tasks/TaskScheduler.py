"""任务编排器：勾选任务，数字越小越先执行（1-30，不可重复）。"""
from src.tasks.BaseOmjTask import BaseOmjTask
from src.tasks.DailyTask import DailyTask
from src.tasks.ExplorationTask import ExplorationTask
from src.tasks.DelegationTask import DelegationTask
from src.tasks.SoulZonesTask import SoulZonesTask
from src.tasks.AreaBossTask import AreaBossTask
from src.tasks.RealmRaidTask import RealmRaidTask
from src.tasks.GameEventsBattleTask import GameEventsBattleTask
from src.tasks.UtilizeTask import UtilizeTask


class TaskScheduler(BaseOmjTask):

    TASK_MAP = {
        "日常-签到": DailyTask,
        "日常-式神委派": DelegationTask,
        "日常-结界": UtilizeTask,
        "日常-战斗-地域鬼王": AreaBossTask,
        "日常-战斗-个人突破": RealmRaidTask,
        "战斗-魂土": SoulZonesTask,
        "战斗-困28": ExplorationTask,
        "战斗-活动": GameEventsBattleTask,
    }

    ALL_TASKS = list(TASK_MAP.keys())

    # 默认顺序
    DEFAULT_ORDER = {name: i + 1 for i, name in enumerate(ALL_TASKS)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "任务编排"
        self.description = "按数字顺序执行日常任务（数字越小越先执行）"

        self.default_config.update({
            "任务列表": self.ALL_TASKS.copy(),
        })
        # 每个任务的顺序数字（1-30）
        for name in self.ALL_TASKS:
            self.default_config[f"{name}顺序"] = self.DEFAULT_ORDER[name]

        self.config_description.update({
            "任务列表": "勾选要执行的任务。",
        })

        self.config_type.update({
            "任务列表": {
                "type": "multi_selection",
                "options": self.ALL_TASKS.copy(),
            },
        })

    def run(self):

        enabled = self.config.get("任务列表", [])

        # 从「一键多任务」获取优先级排序后的任务列表
        from src.ui.MultiTaskTab import get_enabled_in_order
        ordered = get_enabled_in_order()

        for i, name in enumerate(ordered, 1):
            task_cls = self.TASK_MAP.get(name)
            if task_cls is None:
                self.log_warning(f"未找到任务: {name}")
                continue

            self.log_info(f"--- [{i}] 开始: {name} ---")
            t = task_cls(self.executor, self.scene)
            t.after_init(executor=self.executor, scene=self.scene)

            if self.logged_in is False:
                self.log_info("没登陆等待登录")
                if not self.wait_until(condition=lambda:self.base_scene(),
                                time_out=120,pre_action=lambda : self.log_page(),raise_if_not_found=False):
                    self.log_warning("登录失败，请检查环境")
                    return False

            ok = t.run_safe()
            self.log_info(f"--- [{i}] 结束: {name} ---")
            if not ok:
                self.log_warning(f"--- [{i}] {name} 失败，中断后续任务 ---")
                self.pending_tasks = [(j + i, n) for j, n in enumerate(ordered[i - 1:])]
                return False
