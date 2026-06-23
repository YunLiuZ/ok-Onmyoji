import os, sys, cv2
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


def draw_ocr_results(img, results, color=(0, 255, 0)):
    """在图片上画出 OCR 识别框和文字。"""
    for r in results:
        cv2.rectangle(img, (r.x, r.y), (r.x + r.width, r.y + r.height), color, 2)
        cv2.putText(img, f"'{r.name}' {r.confidence:.2f}", (r.x, r.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)


# ============================================================
# 测试1: home/1.png — Find_And_Click_Home('式神录')
# ============================================================
print("=" * 50)
print("测试1: home/1.png — OCR 底部区域 匹配 '式神录'")
print("=" * 50)

IMAGE1 = "tests/img/home/1.png"
ok_test.device_manager.capture_method.set_images([IMAGE1])
frame1 = task.next_frame()
h1, w1 = frame1.shape[:2]

results1 = task.ocr(0, 0.8, 1, 1, match='式神录')
print(f"匹配到 {len(results1)} 个结果:")
for r in results1:
    print(f"  text='{r.name}' conf={r.confidence:.3f} pos=({r.x},{r.y})")

draw_ocr_results(frame1, results1)
cv2.imwrite("tests/img/battle_test1_home.png", frame1)
print("saved: tests/img/battle_test1_home.png\n")


# ============================================================
# 测试2: switchsoul/1.png — 预设界面
# ============================================================
print("=" * 50)
print(f"测试2: switchsoul/1.png — 预设界面")
print(f"  Preset Group = '{task.config['Preset Group']}'")
print(f"  Preset Team  = '{task.config['Preset Team']}'")
print("=" * 50)

IMAGE2 = "tests/img/switchsoul/1.png"
ok_test.device_manager.capture_method.set_images([IMAGE2])
frame2 = task.next_frame()
h2, w2 = frame2.shape[:2]

# Step A: OCR '预设' in Home_Shikigami_Presets region
print("\n--- Step A: 找 '预设' 按钮 ---")
results_a = task.ocr(match='预设', box='Home_Shikigami_Presets')
print(f"匹配到 {len(results_a)} 个结果:")
for r in results_a:
    print(f"  text='{r.name}' conf={r.confidence:.3f} pos=({r.x},{r.y})")
draw_ocr_results(frame2, results_a, (255, 0, 0))

# Step B: OCR Preset Group in Home_Shikigami_Group region
print(f"\n--- Step B: 找预设组 '{task.config['Preset Group']}' ---")
results_b = task.ocr(match=task.config["Preset Group"], box='Home_Shikigami_Group')
print(f"匹配到 {len(results_b)} 个结果:")
for r in results_b:
    print(f"  text='{r.name}' conf={r.confidence:.3f} pos=({r.x},{r.y})")
draw_ocr_results(frame2, results_b, (255, 255, 0))

# Step C: OCR Preset Team in Home_Shikigami_Group_Name region
print(f"\n--- Step C: 找预设队伍 '{task.config['Preset Team']}' ---")
results_c = task.ocr(match=task.config["Preset Team"], box='Home_Shikigami_Group_Name')
print(f"匹配到 {len(results_c)} 个结果:")
for r in results_c:
    center_y = r.y + r.height / 2
    rel_y = center_y / h2
    print(f"  text='{r.name}' conf={r.confidence:.3f} pos=({r.x},{r.y})")
    print(f"    中心Y={center_y:.0f} 相对Y={rel_y:.3f} → click_relative(0.77, {rel_y:.3f})")
    draw_ocr_results(frame2, results_c, (0, 255, 0))

if not results_c:
    print("  (没找到，看看这个区域有哪些文字)")
    all_texts = task.ocr(box='Home_Shikigami_Group_Name')
    for r in all_texts:
        print(f"    text='{r.name}' conf={r.confidence:.3f}")
        draw_ocr_results(frame2, [r], (0, 0, 255))

cv2.imwrite("tests/img/battle_test2_switchsoul.png", frame2)
print("\nsaved: tests/img/battle_test2_switchsoul.png")

destroy_ok()
