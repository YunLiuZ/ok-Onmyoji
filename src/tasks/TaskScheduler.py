"""任务编排器：勾选任务并设优先级后一键启动。"""
from ok import TaskDisabledException, communicate
from src.globals import ALL_TASK_NAMES, TASK_MAP as TM
from src.tasks.BaseOmjTask import BaseOmjTask


class TaskScheduler(BaseOmjTask):

    TASK_MAP = TM
    ALL_TASKS = ALL_TASK_NAMES

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "一键多任务"
        self.description = "勾选任务、设置优先级后启动"
        self._active_task = None


        self.default_config.update({
            "任务列表": self.ALL_TASKS.copy(),
        })
        for name in self.ALL_TASKS:
            self.default_config.update({f"{name}": "20"})

        self.config_description.update({
            "任务列表": "勾选要执行的任务，数字越小，越快执行。",
        })

        self.config_type.update({
            "任务列表": {
                "type": "multi_selection",
                "options": self.ALL_TASKS.copy(),
            },
        })

    def disable(self):
        super().disable()
        if self._active_task is not None:
            self._active_task.disable()
            self._active_task.unpause()

    def run(self):

        enabled = self.config.get("任务列表", [])

        tasks = []
        for name in enabled:
            pri = int(self.config.get(name, "20") or 20)
            idx = ALL_TASK_NAMES.index(name) if name in ALL_TASK_NAMES else 99
            tasks.append((pri, idx, name))
        tasks.sort(key=lambda x: (x[0], x[1]))
        ordered = [t[2] for t in tasks]

        self._clear_flags()

        for i, name in enumerate(ordered, 1):
            if not self.enabled:
                self.log_info("一键多任务已停止")
                break
            task_cls = self.TASK_MAP.get(name)
            if task_cls is None:
                self.log_warning(f"未找到任务: {name}")
                continue
            
            self.log_info(f"--- [{i}] 开始: {name} ---")
            t = task_cls(self.executor, self.scene)
            t.after_init(executor=self.executor, scene=self.scene)
            t._enabled = True
            self._active_task = t
            self.executor.current_task = t
            communicate.task.emit(t)

            try:
                ok = t.run_safe()
            except TaskDisabledException:
                self.log_info(f"--- [{i}] 已停止: {name} ---")
                raise
            finally:
                self._active_task = None
                self.executor.current_task = self
                communicate.task.emit(self)
            self.log_info(f"--- [{i}] 结束: {name} ---")
            if not self.enabled:
                self.log_info("一键多任务已停止")
                break
            if not ok:
                self.log_warning(f"--- [{i}] {name} 失败，继续下一任务 ---")
                continue
