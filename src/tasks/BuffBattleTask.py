import re

from src.tasks.BaseBattleTask import BaseBattleTask

class BuffBattleTask(BaseBattleTask):
    BUFF_NAMES = ["觉醒", "御魂","金币增加50", "金币增加100", "经验增加50", "经验增加100"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_config.update({
            "Buff Enable": [],
            "FindMode": "最近",
        })

        self.config_description.update({
            "Buff Enable": "选择需要打开的加成，不选则不开任何加成。",
            "FindMode": "邀请好友时优先查看哪个标签页:默认顺序（最近/好友/跨区/寮友）。",
        })

        self.config_type.update({
            "Buff Enable": {
                "type": "multi_selection",
                "options": self.BUFF_NAMES.copy(),
            },
            "FindMode": {
                "type": "drop_down",
                "options": ["最近", "好友", "跨区", "寮友"],
            },
        })