from ok import TriggerTask

from src.tasks.BaseOmjTask import BaseOmjTask
from src.tasks.DailyTask import DailyTask
from src.tasks.ExplorationTask import ExplorationTask
from src.tasks.DelegationTask import DelegationTask
from src.tasks.SoulZonesTask import SoulZonesTask
from src.tasks.AreaBossTask import AreaBossTask
from src.tasks.RealmRaidTask import RealmRaidTask
from src.tasks.GameEventsBattleTask import GameEventsBattleTask
from src.tasks.UtilizeTask import UtilizeTask


class MyTriggerTask(TriggerTask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "触发器会不断调用run方法"
        self.description = "一般根据frame来判断是否需要运行"
        self.trigger_interval = 1       # 每秒调一次 run()
        self.trigger_count = 0
        self.default_config = {'_enabled': True}
        

    def run(self):
        self.trigger_count += 1
        print(self.trigger_count)
        self.log_debug(f'MyTriggerTask run {self.trigger_count}')