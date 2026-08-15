import os, sys, cv2, types
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
IMAGE = "tests/img/2.png"
ok_test.device_manager.capture_method.set_images([IMAGE])
frame = task.next_frame()
h, w = frame.shape[:2]

# ---- 拦截 click，记录实际点击的像素坐标（不真正点屏幕）----
# click_box 最终以像素坐标调用 self.click(x, y)；x/y > 1 说明是像素坐标而非 0~1 相对坐标
clicked_points = []
def recording_click(self, x=-1, y=-1, *args, **kwargs):
    if isinstance(x, (int, float)) and x > 1 and y > 1:
        clicked_points.append((int(x), int(y)))
    return True
task.click = types.MethodType(recording_click, task)

# ---- 配置：特征名 + 搜索区域 + 随机点击次数 ----
searches = [
    ("Home_Explore", task.box_of_screen(0.45, 0.09, 0.73, 0.57), 3),
]

for name, region, times in searches:
    # 1. 画搜索区域（蓝色）
    cv2.rectangle(frame, (region.x, region.y),
                  (region.x + region.width, region.y + region.height), (255, 0, 0), 2)
    cv2.putText(frame, f"{name} search", (region.x + 5, region.y + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    # 2. 画匹配框（绿色）
    boxes = task.find_feature(name, threshold=0.8, box=region)
    if boxes:
        for b in boxes:
            print(f"MATCH {name}: conf={b.confidence:.4f} box=({b.x},{b.y},{b.width},{b.height})")
            cv2.rectangle(frame, (b.x, b.y), (b.x + b.width, b.y + b.height), (0, 255, 0), 3)
    else:
        print(f"MISS  {name}")

    # 3. 多次调用 wait_click_feature，收集随机点击点
    clicked_points.clear()
    for _ in range(times):
        task.wait_click_feature(name, threshold=0.8, box=region,
                                raise_if_not_found=False, time_out=2, after_sleep=0)

    # 4. 画点击点（红色圆点 + 十字）
    for (cx, cy) in clicked_points:
        cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
        cv2.drawMarker(frame, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 20, 2)
    print(f"clicked {name}: {clicked_points}")

cv2.imwrite("tests/img/test6_out.png", frame)
print("saved tests/img/test6_out.png")

# ---- OCR 版本示例：测 wait_click_ocr / ocr_and_click 的随机点击 ----
# 取消注释，把 match 和 box 改成你要测的文字和区域：
# clicked_points.clear()
# for _ in range(10):
#     task.wait_click_ocr(match="预设",
#                         box=task.box_of_screen(0.02, 0.87, 0.14, 1.0),
#                         raise_if_not_found=False, time_out=2, after_sleep=0)
# for (cx, cy) in clicked_points:
#     cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)

destroy_ok()
