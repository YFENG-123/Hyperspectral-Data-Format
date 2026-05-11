"""
GT Statistics Analyzer
=======================
统计 .mat 格式 Ground Truth 文件的：
  1. 每个 ID（类别）的像素数量（含背景 0）
  2. 每个 ID（类别）的连通区域数量

使用方法：
  在脚本顶部的 MAT_FILE 变量中填入 .mat 文件路径，然后运行脚本。
  结果输出到同目录下的 gt_statistics_results/ 文件夹中。
"""

import os
import shutil
import scipy.io as sio
import numpy as np
from scipy import ndimage
from datetime import datetime

# ============================================================
# TODO: 填入你的 .mat 格式 Ground Truth 文件路径
# ============================================================
MAT_FILE = r"Pavia\\Pavia_gt.mat"
# ============================================================

# --- 自动检测 .mat 中的数据键名（跳过 __header__ 等元数据键）---
def _get_data_from_mat(mat_path):
    mat_dict = sio.loadmat(mat_path)
    data_key = None
    data = None
    for k, v in mat_dict.items():
        if k.startswith("__"):
            continue
        data = v
        data_key = k
        break
    if data_key is None:
        raise ValueError(f"无法从 {mat_path} 中找到数据数组")
    return data, data_key


def _pixel_count_per_id(data):
    """统计每个 ID 的像素数量"""
    unique_ids = np.unique(data)
    counts = {}
    total = data.size
    for uid in unique_ids:
        counts[int(uid)] = int(np.sum(data == uid))
    return counts, total


def _region_count_per_id(data):
    """统计每个 ID 的连通区域数量（4邻接）"""
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])  # 4邻接
    unique_ids = np.unique(data)
    unique_ids = unique_ids[unique_ids > 0]  # 排除背景0
    counts = {}
    for uid in unique_ids:
        mask = (data == uid).astype(int)
        _, num = ndimage.label(mask, structure=structure)
        counts[int(uid)] = num
    return counts


def _format_table(rows, headers, col_widths):
    """将表格行格式化为对齐的纯文本字符串"""
    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    sep = "  ".join("-" * w for w in col_widths)
    lines = [header_line, sep]
    for row in rows:
        lines.append("  ".join(str(v).ljust(w) for v, w in zip(row, col_widths)))
    return "\n".join(lines)


def main():
    # --- 验证输入文件 ---
    if not os.path.isfile(MAT_FILE):
        print(f"[错误] 文件不存在: {MAT_FILE}")
        print("请修改脚本顶部的 MAT_FILE 变量，填入正确的 .mat 文件路径。")
        return

    print(f"\n正在加载: {MAT_FILE}")
    data, data_key = _get_data_from_mat(MAT_FILE)
    print(f"数据键名: '{data_key}'，形状: {data.shape}，数据类型: {data.dtype}")

    # --- 统计 ---
    pixel_counts, total_pixels = _pixel_count_per_id(data)
    region_counts = _region_count_per_id(data)

    # --- 构建输出目录 ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mat_basename = os.path.splitext(os.path.basename(MAT_FILE))[0]
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = os.path.join(script_dir, "gt_statistics_results", f"{mat_basename}_{ts}")
    os.makedirs(out_dir, exist_ok=True)

    # ========== 输出 1：像素统计 ==========
    # 表头
    headers = ["ID", "像素数", "占比 (%)", "类别"]
    rows = []
    for uid in sorted(pixel_counts.keys()):
        cnt = pixel_counts[uid]
        pct = cnt / total_pixels * 100
        label = "背景" if uid == 0 else f"类别 {uid}"
        rows.append([uid, cnt, f"{pct:.2f}", label])

    col_widths = [max(len(headers[i]), max(len(str(r[i])) for r in rows) + 2) for i in range(4)]
    table = _format_table(rows, headers, col_widths)

    result1_path = os.path.join(out_dir, "pixel_count.txt")
    with open(result1_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("GT 像素统计（Pixel Count per ID）\n")
        f.write("=" * 60 + "\n")
        f.write(f"文件: {MAT_FILE}\n")
        f.write(f"数据键名: {data_key}  形状: {data.shape}  总像素: {total_pixels}\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 60 + "\n")
        f.write(table)
        f.write("\n")

    # ========== 输出 2：连通区域统计 ==========
    all_ids = sorted(region_counts.keys())
    rows2 = [[uid, region_counts[uid]] for uid in all_ids]

    col_widths2 = [max(8, max(len(str(r[i])) for r in rows2) + 2) for i in range(2)]
    headers2 = ["ID", "区域数"]
    table2 = _format_table(rows2, headers2, col_widths2)

    result2_path = os.path.join(out_dir, "region_count.txt")
    with open(result2_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("GT 连通区域统计（Region Count per ID）\n")
        f.write("=" * 60 + "\n")
        f.write(f"文件: {MAT_FILE}\n")
        f.write(f"数据键名: {data_key}  形状: {data.shape}\n")
        f.write(f"连通性: 4邻接（上下左右）\n")
        f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 60 + "\n")
        f.write(table2)
        f.write("\n")

    # ========== 控制台打印摘要 ==========
    print(f"\n{'='*60}")
    print("GT 像素统计（Pixel Count per ID）")
    print("=" * 60)
    print(table)
    print(f"\n总像素数: {total_pixels}")

    print(f"\n{'='*60}")
    print("GT 连通区域统计（Region Count per ID）")
    print("=" * 60)
    print(table2)
    print(f"\n{'='*60}")
    print(f"结果已保存至: {out_dir}")
    print(f"  1. pixel_count.txt  - 像素统计")
    print(f"  2. region_count.txt  - 连通区域统计")


if __name__ == "__main__":
    main()
