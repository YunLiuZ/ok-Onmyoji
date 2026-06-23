"""测试 Home_Shikigami_Group_Name 区域的 OCR 识别结果。"""
import os, sys, cv2, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from ok.test import init_ok, destroy_ok

config["debug"] = True
config["trigger_tasks"] = []
init_ok(config)

from ok import og
from src.tasks.BaseBattleTask import BaseBattleTask
from ok.test import ok as ok_test

task = BaseBattleTask(og.executor, None)
task.feature_set = ok_test.feature_set
task.after_init(executor=ok_test.task_executor, scene=ok_test.task_executor.scene)

IMAGE = "tests/img/switchsoul/1.png"
ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()

# ---- OCR Home_Shikigami_Group_Name 区域 ----
box = task.get_box_by_name("Home_Shikigami_Group_Name")
texts = task.ocr(box=box, frame=frame)

print(f"Region: Home_Shikigami_Group_Name")
print(f"  position: ({box.x}, {box.y}) size: {box.width}x{box.height}")
print(f"  OCR results: {len(texts)}")
print()

for i, t in enumerate(texts, 1):
    print(f"  {i}. [{t.name}] conf={t.confidence:.3f}  pos=({t.x},{t.y})  size={t.width}x{t.height}")

# 画图
for t in texts:
    cv2.rectangle(frame, (t.x, t.y), (t.x + t.width, t.y + t.height), (0, 255, 0), 2)
    cv2.putText(frame, f"'{t.name}' {t.confidence:.2f}", (t.x, t.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

cv2.imwrite("tests/img/ocr_group_name_result.png", frame)
print(f"\nsaved: tests/img/ocr_group_name_result.png")

destroy_ok()
