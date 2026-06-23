"""详细测试：标注 BOX 搜索区域 + COCO 中心点 + 实际匹配结果。

用法:
    python tests/test_boxes_detail.py --test signcancel  # Daily_New_Cancel / Cancel_Old
    python tests/test_boxes_detail.py --test home        # Home_Town / Store / Sign
    python tests/test_boxes_detail.py --test store       # Gift_Store / Grocery_Store / Gift_Daily
    python tests/test_boxes_detail.py --test backhome    # Back / Home_Button
"""
import os, sys, cv2, json
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

# ---- 加载 COCO 中心参考 ----
with open("assets/coco_annotations.json") as f:
    coco = json.load(f)
img_map = {i["id"]: i for i in coco["images"]}


def get_coco_center(name):
    cat = next((c for c in coco["categories"] if c["name"] == name), None)
    if cat is None:
        return None
    ann = next((a for a in coco["annotations"] if a["category_id"] == cat["id"]), None)
    if ann is None:
        return None
    img = img_map[ann["image_id"]]
    x, y, w, h = ann["bbox"]
    return {
        "rel": (x + w / 2) / img["width"],  # 相对 X
        "rely": (y + h / 2) / img["height"],  # 相对 Y
        "src": img["file_name"],
        "bbox": (x, y, w, h),
    }


def draw_coco_center(img, name, w, h, color=(0, 165, 255)):
    """画出 COCO 标注的中心点位置。"""
    info = get_coco_center(name)
    if info is None:
        return
    cx = int(info["rel"] * w)
    cy = int(info["rely"] * h)
    cv2.drawMarker(img, (cx, cy), color, cv2.MARKER_CROSS, 20, 2)
    cv2.putText(img, f"COCO {name}", (cx + 10, cy - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
    print(f"  COCO center: ({info['rel']:.4f}, {info['rely']:.4f}) -> pixel({cx},{cy})  src={info['src']}")


# ---- 测试场景 ----
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--test", default="signcancel",
                    choices=["signcancel", "home", "store", "backhome"])
args = parser.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def path(p):
    return os.path.join(ROOT, p)

scenes = {
    "signcancel": (path("tests/img/home/signcancel.png"),
                   ["Daily_New_Cancel", "Cancel_Old"],
                   path("tests/img/boxes_detail_signcancel.png")),
    "home":       (path("tests/img/home/1.png"),
                   ["Home_Town", "Home_Store", "Home_Sign"],
                   path("tests/img/boxes_detail_home.png")),
    "store":      (path("tests/img/home/store.png"),
                   ["Gift_Store", "Grocery_Store", "Gift_Daily"],
                   path("tests/img/boxes_detail_store.png")),
    "backhome":   (path("tests/img/home/store.png"),
                   ["Back", "Home_Button"],
                   path("tests/img/boxes_detail_backhome.png")),
}

IMAGE, features, OUTPUT = scenes[args.test]
colors = [(255, 0, 0), (255, 255, 0), (0, 255, 255)]

ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()
h, w = frame.shape[:2]
print(f"Image: {IMAGE} ({w}x{h})")
print()

for name, color in zip(features, colors):
    print(f"--- {name} ---")
    # 1. COCO 中心（橙色十字）
    draw_coco_center(frame, name, w, h, (0, 165, 255))

    # 2. BOX 搜索区域（蓝/黄/青框）
    region = task.B(name)
    cv2.rectangle(frame, (region.x, region.y),
                  (region.x + region.width, region.y + region.height), color, 2)
    cv2.putText(frame, f"{name} search", (region.x + 5, region.y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # 3. 实际匹配
    box = task.find_one(name, threshold=0.5, box=region)
    if box:
        actual_cx = (box.x + box.width // 2) / w
        actual_cy = (box.y + box.height // 2) / h
        print(f"  MATCH: conf={box.confidence:.4f}  pos=({box.x},{box.y})  size={box.width}x{box.height}")
        print(f"         实际中心: ({actual_cx:.4f}, {actual_cy:.4f})")
        cv2.rectangle(frame, (box.x, box.y),
                      (box.x + box.width, box.y + box.height), (0, 255, 0), 3)
        cv2.putText(frame, f"{name} {box.confidence:.2f}", (box.x, box.y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        print(f"  MISS (threshold=0.5)")
    print()

cv2.imwrite(OUTPUT, frame)
print(f"saved: {OUTPUT}")
print("Orange cross=COCO center  Colored box=search region  Green box=matched result")

destroy_ok()
