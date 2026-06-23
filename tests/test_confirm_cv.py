"""cv2 全图搜索 Confirm 模板，可视化结果。"""
import json, cv2

with open("assets/coco_annotations.json") as f:
    coco = json.load(f)

# 找到 Confirm 的标注
cat = next(c for c in coco["categories"] if c["name"] == "Confirm")
ann = next(a for a in coco["annotations"] if a["category_id"] == cat["id"])
img_entry = next(i for i in coco["images"] if i["id"] == ann["image_id"])

# 裁剪模板
src = cv2.imread(f"assets/{img_entry['file_name']}")
x, y, w, h = ann["bbox"]
template = src[y : y + h, x : x + w]
print(f"Template: {img_entry['file_name']} bbox=({x},{y},{w},{h})")

# 加载测试图
frame = cv2.imread("tests/img/home/confirm.png")
fh, fw = frame.shape[:2]
print(f"Test image: {fw}x{fh}")

# ===== 方法1: 限定搜索区域 (0.33, 0.52, 0.71, 0.65) =====
rx1, ry1 = int(0.33 * fw), int(0.52 * fh)
rx2, ry2 = int(0.71 * fw), int(0.65 * fh)
roi = frame[ry1:ry2, rx1:rx2]
result1 = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
_, max_val1, _, max_loc1 = cv2.minMaxLoc(result1)
# 转回原图坐标
mx1, my1 = max_loc1[0] + rx1, max_loc1[1] + ry1
print(f"\nRegion search (0.33,0.52~0.71,0.65): best={max_val1:.4f} pos=({mx1},{my1})")
cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (255, 0, 0), 2)  # 蓝色=搜索区域
if max_val1 >= 0.6:
    print("  MATCH")
    color = (0, 255, 0)
else:
    print("  MISS")
    color = (0, 0, 255)
cv2.rectangle(frame, (mx1, my1), (mx1 + w, my1 + h), color, 3)

# ===== 方法2: 全图搜索 =====
result2 = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
_, max_val2, _, max_loc2 = cv2.minMaxLoc(result2)
mx2, my2 = max_loc2
print(f"\nFull image search: best={max_val2:.4f} pos=({mx2},{my2})")
cv2.circle(frame, (mx2 + w // 2, my2 + h // 2), 5, (0, 255, 255), -1)
if max_val2 >= 0.6:
    print("  MATCH")
    cv2.rectangle(frame, (mx2, my2), (mx2 + w, my2 + h), (0, 255, 255), 3)
    cv2.putText(frame, f"Confirm {max_val2:.2f}", (mx2, my2 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
else:
    print("  MISS")

cv2.putText(frame, "Blue=search region", (rx1 + 5, ry1 + 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
cv2.imwrite("tests/img/confirm_cv_result.png", frame)
print("\nsaved: tests/img/confirm_cv_result.png")
