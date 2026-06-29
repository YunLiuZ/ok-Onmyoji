"""测试 Back_Home 函数：传入一张不在主页的图，观察 try_back 的匹配过程。"""
import os, sys, cv2
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# ---- 选一张不在主页的图 ----
IMAGE = os.path.join(ROOT, "tests/img/home/store.png")  # 商店截图，不是主页
ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()
h, w = frame.shape[:2]
print(f"Image: {w}x{h}")

# 先确认不在主页
print(f"In_Home = {task.In_Home()}")
print()

# 运行 Back_Home（静态图不会真的回主页，20s 后会超时）
print("Back_Home() ...")
result = task.Back_Home()
print(f"Back_Home result: {result}")
print(f"In_Home after: {task.In_Home()}")

# 画图：标记 try_back 中涉及的搜索区域
for name, color in [
    ("Home_Button", (255, 0, 0)),
    ("Cancel_Old", (255, 255, 0)),
    ("Daily_New_Cancel", (0, 255, 255)),
    ("Back", (255, 0, 255)),
]:
    region = task.B(name)
    cv2.rectangle(frame, (region.x, region.y),
                  (region.x + region.width, region.y + region.height), color, 2)
    box = task.find_one(name, threshold=0.5, box=task.B("full"))
    if box:
        print(f"  {name}: conf={box.confidence:.3f} at ({box.x},{box.y})")
        cv2.rectangle(frame, (box.x, box.y),
                      (box.x + box.width, box.y + box.height), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} {box.confidence:.2f}", (box.x, box.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

out = os.path.join(ROOT, "tests/img/back_home_test.png")
cv2.imwrite(out, frame)
print(f"\nsaved: tests/img/back_home_test.png")

destroy_ok()
