import time
import logging
import ok
from src.config import config

if __name__ == '__main__':
    class Id_f(logging.Filter):
        def filter(self, record):
            return "player id check failed" not in record.getMessage()
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
    ok = ok.OK(config)
    ok.start()
