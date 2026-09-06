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

    # 修复 multi_selection 排版挤：调大 FlowLayout 列数
    try:
        from ok.ui.qt.tasks.LabelAndMultiSelection import LabelAndMultiSelection
        _original_ms_init = LabelAndMultiSelection.__init__

        def patched_ms_init(self, config_desc, options, config, key):
            _original_ms_init(self, config_desc, options, config, key)
            if hasattr(self, 'content_layout'):
                self.content_layout.max_columns = 3
                self.content_layout._rebuild()

        LabelAndMultiSelection.__init__ = patched_ms_init
    except Exception:
        pass

    config = config

    # 多开日志分离：按 instance_id 分目录 logs/{id}/ok-script.log
    import os
    _original_config_logger = ok.config_logger
    def patched_config_logger(cfg=None, name='ok-script'):
        iid = cfg.get('instance_id', 1) if cfg else 1
        return _original_config_logger(cfg, os.path.join(str(iid), 'ok-script'))
    ok.config_logger = patched_config_logger
    # 多开 PC 窗口识别：当 windows.exe 配置了多个同进程窗口(如 onmyoji.exe)时,
    # 每次都把匹配窗口全部列成独立设备 pc_{hwnd}, 供 UI 选择, 根据 hwnd 区分不同窗口。
    # 用户点选某个窗口后框架会把其 hwnd 写进 config['selected_hwnd'],
    # 此时代理返回该窗口的 imei 供 update_capture 精确锁定, 不影响多窗口列表。
    try:
        from ok.device.DeviceManager import DeviceManager
        from ok.util.window import find_all_visible_windows, get_window_bounds
        import win32gui

        _original_update_pc_device = DeviceManager.update_pc_device


        def patched_update_pc_device(self):
            cfg = getattr(self, 'windows_capture_config', None)
            exe_list = cfg.get('exe') if cfg else None
            if not exe_list:
                return _original_update_pc_device(self)
            if isinstance(exe_list, str):
                exe_list = [exe_list]
            exe_list = [e.lower() for e in exe_list]
            hwnd_class = cfg.get('hwnd_class')
            selected_hwnd = self.config.get('selected_hwnd')
            pc_devices = {}
            selected_imei = None
            for hwnd, title, exe_name, full_path in find_all_visible_windows():
                try:
                    if not exe_name or exe_name.lower() not in exe_list:
                        continue
                    if hwnd_class:
                        cname = win32gui.GetClassName(hwnd)
                        if cname != hwnd_class:
                            continue
                    x, y, _, _, width, height, _ = get_window_bounds(hwnd)
                    if width <= 10 or height <= 10:
                        continue
                    imei = f"pc_{hwnd}"
                    pc_devices[imei] = {
                        "address": "", "imei": imei, "device": "windows",
                        "model": "", "nick": f"{title} #{hwnd}", "width": width,
                        "height": height, "hwnd": f"{title} #{hwnd}", "capture": "windows",
                        "connected": True, "full_path": full_path,
                        "real_hwnd": hwnd, "exe": exe_list,
                        "resolution": f"{width}x{height}",
                    }
                    if selected_hwnd and hwnd == selected_hwnd:
                        selected_imei = imei
                except Exception:
                    continue
            if pc_devices:
                self._replace_pc_devices(pc_devices)
                return selected_imei
            return _original_update_pc_device(self)


        DeviceManager.update_pc_device = patched_update_pc_device
    except Exception:
        pass

    ok = ok.OK(config)
    ok.start()
