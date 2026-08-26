import time
import logging
import ok
from src.config import config

if __name__ == '__main__':
    class Id_f(logging.Filter):
        def filter(self, record):
            msg = record.getMessage()
            return ("player id check failed" not in msg
                    and "get_exe_by_hwnd" not in msg)
    logging.getLogger("ok").addFilter(Id_f())
    config = config
    config['debug'] = True


    # 多开日志分离：按 instance_id 分目录 logs/{id}/ok-script.log
    import os
    _original_config_logger = ok.config_logger
    def patched_config_logger(cfg=None, name='ok-script'):
        iid = cfg.get('instance_id', 1) if cfg else 1
        return _original_config_logger(cfg, os.path.join(str(iid), 'ok-script'))
    ok.config_logger = patched_config_logger

    ok = ok.OK(config)
    ok.start()
