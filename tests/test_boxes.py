"""测试 feature_boxes.py 中的搜索区域是否正确。

用法:
    python tests/test_boxes.py                  # 默认: home/1.png 测 Home_Town/Store/Sign
    python tests/test_boxes.py --test store     # store.png 测 Gift_Store/Grocery_Store/Gift_Daily
"""
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

# ---- 测试场景 ----
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--test", default="store", choices=["home", "store"])
args = parser.parse_args()

if args.test == "store":
    IMAGE = "tests/img/home/giftd.png"
    features = ["Gift_Store", "Grocery_Store", "Gift_Finish"]
    OUTPUT = "tests/img/boxes_test_store.png"
else:
    IMAGE = "tests/img/home/1.png"
    features = ["Home_Town", "Home_Store", "Home_Sign"]
    OUTPUT = "tests/img/boxes_test.png"

ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255)]

for name, color in zip(features, colors):
    region = task.B(name)
    cv2.rectangle(frame, (region.x, region.y),
                  (region.x + region.width, region.y + region.height), color, 2)
    cv2.putText(frame, f"{name} search", (region.x + 5, region.y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    box = task.find_one(name, threshold=0.6, box=region)
    if box:
        print(f"MATCH {name}: conf={box.confidence:.4f} pos=({box.x},{box.y})")
        cv2.rectangle(frame, (box.x, box.y),
                      (box.x + box.width, box.y + box.height), (0, 255, 0), 3)
        cv2.putText(frame, f"{name} {box.confidence:.2f}", (box.x, box.y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        print(f"MISS  {name}")

cv2.imwrite(OUTPUT, frame)
print(f"\nsaved: {OUTPUT}")

destroy_ok()
