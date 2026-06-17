import os, sys, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# ---- 设置测试图片 ----
IMAGE = "tests/img/home/1.png"
ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()

# ---- 核心：找特征 ----
box1 = task.find_one("Daily_New_Cancel", threshold=0.6, box=task.box_of_screen(0.7, 0, 1, 0.5))
box2 = task.find_one("Home_Button", threshold=0.6, box=task.box_of_screen(0.7, 0, 1, 0.5))
box3 = task.find_one("Back", threshold=0.6, box=task.box_of_screen(0.7, 0, 1, 0.5))

# ---- 画结果 ----
for box, name in [(box1, "Daily_New_Cancel"), (box2, "Home_Button"), (box3, "Back")]:
    if box:
        print(f"MATCH {name}: conf={box.confidence:.4f} pos=({box.x},{box.y})")
        cv2.rectangle(frame, (box.x, box.y), (box.x + box.width, box.y + box.height), (0, 255, 0), 3)
        cv2.putText(frame, f"{name} {box.confidence:.2f}", (box.x, box.y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        print(f"MISS  {name}")

cv2.imwrite("tests/img/2.png", frame)
print("saved to tests/img/2.png")

destroy_ok()
