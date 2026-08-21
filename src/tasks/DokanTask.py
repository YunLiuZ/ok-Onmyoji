import re
import random

from src.tasks.BaseBattleTask import BaseBattleTask


class GateTask(BaseBattleTask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "日常-寮内-道馆"
        self.description = "暂未完成，先挖坑"
        self.default_config.update({

        })
        self.config_description.update({

        })
    def run(self):
        pass