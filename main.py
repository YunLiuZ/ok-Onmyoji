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

    # 窗口闪烁容差: 检测到窗口消失/尺寸变化时, 等0.3秒确认稳定后再决定
    import ok.device.capture_methods.hwnd_window as hwnd_mod
    _original_do_update = hwnd_mod.HwndWindow.do_update_window_size

    def patched_do_update(self):
        pre_visible = self.visible
        pre_width = self.width
        pre_height = self.height
        _original_do_update(self)
        # 窗口从可见→不可见 或 尺寸变化 → 二次确认
        if pre_visible and (not self.visible or
                            self.width != pre_width or self.height != pre_height):
            time.sleep(0.3)
            _original_do_update(self)
            if self.visible and self.device_manager and self.device_manager.executor:
                try:
                    self.device_manager.executor.resume()
                except Exception:
                    pass

    hwnd_mod.HwndWindow.do_update_window_size = patched_do_update

    config = config

    # 多开日志分离：按 instance_id 分目录 logs/{id}/ok-script.log
    import os
    _original_config_logger = ok.config_logger
    def patched_config_logger(cfg=None, name='ok-script'):
        iid = cfg.get('instance_id', 1) if cfg else 1
        return _original_config_logger(cfg, os.path.join(str(iid), 'ok-script'))
    ok.config_logger = patched_config_logger

    ok = ok.OK(config)
    ok.start()
