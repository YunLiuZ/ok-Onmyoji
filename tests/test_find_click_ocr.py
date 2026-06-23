"""测试 Find_And_Click_Home OCR 识别 — 搜"商店"并标记点击位置。"""
import os, sys, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from src.config import config
from ok.test import init_ok, destroy_ok

config["debug"] = True
config["trigger_tasks"] = []
init_ok(config)

from ok import og
from src.tasks.DailyTask import DailyTask
from ok.test import ok as ok_test

task = DailyTask(og.executor, None)
task.feature_set = ok_test.feature_set
task.after_init(executor=ok_test.task_executor, scene=ok_test.task_executor.scene)

IMAGE = os.path.join(PROJECT, "tests/img/home/1.png")
ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()
h, w = frame.shape[:2]

# ---- OCR 底部区域搜"商店" ----
texts = task.ocr(0, 0.8, 1, 1, match="商店")
print(f"OCR '商店': {len(texts)} results")

# 画搜索区域（蓝色）
cv2.rectangle(frame, (0, int(0.8 * h)), (w, h), (255, 0, 0), 2)
cv2.putText(frame, "OCR search (0,0.8~1,1)", (5, int(0.8 * h) + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

for t in texts:
    print(f"  [{t.name}] conf={t.confidence:.3f} pos=({t.x},{t.y}) size={t.width}x{t.height}")
    # 识别框（绿）
    cv2.rectangle(frame, (t.x, t.y), (t.x + t.width, t.y + t.height), (0, 255, 0), 2)
    cx, cy = t.x + t.width // 2, t.y + t.height // 2
    # 点击位置十字线（红）
    cv2.drawMarker(frame, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 15, 2)
    cv2.putText(frame, t.name, (t.x, t.y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    print(f"  点击位置: ({cx}, {cy})")

OUT = os.path.join(PROJECT, "tests/img/ocr_shop_test.png")
cv2.imwrite(OUT, frame)
print(f"\nsaved: tests/img/ocr_shop_test.png")

destroy_ok()
