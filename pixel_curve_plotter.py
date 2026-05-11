"""
将 .mat 格式高光谱数据中每个像素点的所有波段值绘制成曲线，
按 ground truth 类别 ID 分文件夹保存。
"""

import os, sys, shutil
import scipy.io as sio
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
from tqdm import tqdm

# ===== 配置 =====
MAT_FILE = r"HuaiL_2\HuaiL_2.mat"
GT_FILE  = r"HuaiL_2\HuaiL_2_gt.mat"

# ===== 验证输入 =====
if not os.path.isfile(MAT_FILE):
    print(f"[错误] 文件不存在: {MAT_FILE}"); sys.exit(1)
if not os.path.isfile(GT_FILE):
    print(f"[错误] 文件不存在: {GT_FILE}"); sys.exit(1)

print(f"\n{'='*60}\n高光谱像素曲线绘制器\n{'='*60}")
print(f"数据文件: {MAT_FILE}\nGT 文件:  {GT_FILE}")

# ===== 加载数据 =====
def load_mat(path):
    d = sio.loadmat(path)
    for k, v in d.items():
        if not k.startswith("__"):
            return v, k
    raise ValueError(f"无法从 {path} 中找到数据数组")

data, dkey = load_mat(MAT_FILE)
gt_data, gkey = load_mat(GT_FILE)
print(f"数据键名: '{dkey}'\nGT 键名:  '{gkey}'")

# ===== 维度处理 =====
if data.ndim == 2:
    h, w = data.shape; c = 1
    data_float = data.astype(np.float32)[..., np.newaxis]
elif data.ndim == 3:
    data_float = data.astype(np.float32)
    h, w, c = data_float.shape
else:
    raise ValueError(f"数据维度异常: {data.ndim}D")

if gt_data.shape != (h, w):
    if gt_data.size == h * w:
        gt_data = gt_data.reshape(h, w)
    else:
        print("[错误] GT 像素数与图像不匹配"); sys.exit(1)

print(f"图像尺寸: H={h}, W={w}, C={c} 波段")
print(f"GT ID 分布: {dict(zip(*np.unique(gt_data, return_counts=True)))}")
total_pixels = h * w

# ===== 全局极值 =====
vmin = 0.0
vmax = 0.4e4
print(f"Y 轴范围: [0, {vmax:.0f}]")

band_indices = np.arange(c, dtype=np.int32)

# ===== 颜色映射 =====
unique_ids = sorted(np.unique(gt_data))
palette = ["#2196F3","#FF5722","#4CAF50","#9C27B0","#FFEB3B",
           "#00BCD4","#E91E63","#8BC34A","#3F51B5","#FF9800",
           "#795548","#607D8B","#F44336","#009688","#CDDC39",
           "#673AB7","#03A9F4","#FFC107","#009688","#8B0000"]
color_map = {uid: palette[i % len(palette)] for i, uid in enumerate(unique_ids)}

# ===== 输出目录 =====
script_dir = os.path.dirname(os.path.abspath(__file__))
ts = datetime.now().strftime("%Y%m%d-%H%M%S")
out_dir = os.path.join(script_dir, "pixel_curve_results",
                       f"{os.path.splitext(os.path.basename(MAT_FILE))[0]}_{ts}")
pixel_img_dir = os.path.join(out_dir, "pixel_curves")
os.makedirs(pixel_img_dir, exist_ok=True)
for uid in unique_ids:
    os.makedirs(os.path.join(pixel_img_dir, f"id_{uid}"), exist_ok=True)

# ===== 概览图 =====
overview_path = os.path.join(out_dir, "00_overview.png")
n_sample = min(500, total_pixels)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 第0波段灰度图
band0 = data_float[:, :, 0]
bv = band0.astype(np.float64).flatten()
bv = bv[np.isfinite(bv)]
v0min = float(np.min(bv)) if bv.size else 0.0
v0max = float(np.max(bv)) if bv.size else 1.0
axes[0].imshow(band0, cmap="gray", vmin=v0min, vmax=v0max)
axes[0].set_title(f"Band 0 (H={h}, W={w}, C={c})", fontsize=11)
axes[0].axis("off")

# 随机曲线叠加
rng = np.random.default_rng(42)
indices = rng.choice(total_pixels, size=n_sample, replace=False)
flat_data = data_float.reshape(-1, c)
for row in flat_data[indices]:
    axes[1].plot(band_indices, row, alpha=0.25, linewidth=0.6)
axes[1].set_xlabel("Band Index"); axes[1].set_ylabel("Pixel Value")
axes[1].set_title(f"Random {n_sample} Pixel Curves (Overlay)", fontsize=11)
axes[1].set_xlim(band_indices[0], band_indices[-1])
axes[1].set_ylim(vmin, vmax)
axes[1].grid(True, alpha=0.3, linestyle="--")
axes[1].ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
fig.suptitle(f"Overview — {os.path.basename(MAT_FILE)}", fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig(overview_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n[概览图] {overview_path}")

# ===== 每个 ID 的平均曲线 =====
# 合在一起
all_fig, all_ax = plt.subplots(figsize=(12, 5))
for uid in unique_ids:
    mask = gt_data.flatten() == uid
    avg_curve = flat_data[mask].mean(axis=0)
    label = "Background" if uid == 0 else f"Class {uid}"
    all_ax.plot(band_indices, avg_curve, color=color_map[uid],
                linewidth=1.5, alpha=0.9, label=f"{label} (ID={uid}, n={mask.sum()})")
all_ax.set_xlabel("Band Index", fontsize=10)
all_ax.set_ylabel("Pixel Value", fontsize=10)
all_ax.set_title(f"Mean Pixel Curve per GT ID — {os.path.basename(MAT_FILE)}",
                 fontsize=12, fontweight="bold")
all_ax.set_xlim(band_indices[0], band_indices[-1])
all_ax.set_ylim(vmin, vmax)
all_ax.grid(True, alpha=0.3, linestyle="--")
all_ax.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
all_ax.legend(fontsize=8, loc="upper right", ncol=2)
all_fig.tight_layout()
all_fig.savefig(os.path.join(out_dir, "01_mean_all.png"), dpi=150, bbox_inches="tight")
plt.close(all_fig)
print(f"  [平均曲线] 合集: {os.path.join(out_dir, '01_mean_all.png')}")

# 单独保存每张
for uid in unique_ids:
    mask = gt_data.flatten() == uid
    avg_curve = flat_data[mask].mean(axis=0)
    label = "Background" if uid == 0 else f"Class {uid}"
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(band_indices, avg_curve, color=color_map[uid], linewidth=2)
    ax.set_xlabel("Band Index", fontsize=10)
    ax.set_ylabel("Pixel Value", fontsize=10)
    ax.set_title(f"{label} (ID={uid}) — Mean Curve, n={mask.sum()} pixels",
                 fontsize=12, fontweight="bold")
    ax.set_xlim(band_indices[0], band_indices[-1])
    ax.set_ylim(vmin, vmax)
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
    fig.tight_layout()
    path = os.path.join(out_dir, f"01_mean_id{uid:02d}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  [平均曲线] ID={uid}: {path}")

# ===== 逐像素绘图 =====
print(f"\n正在逐像素绘制曲线（共 {total_pixels} 个）\n图片将保存至: {pixel_img_dir}\n")
pbar = tqdm(total=total_pixels, desc="绘制进度", unit="px")

for i in range(h):
    for j in range(w):
        gt_id = int(gt_data[i, j])
        pixel_values = np.clip(data_float[i, j, :], vmin, vmax)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(band_indices, pixel_values, color=color_map[gt_id], linewidth=1.2, alpha=0.85)
        ax.set_xlabel("Band Index", fontsize=10)
        ax.set_ylabel("Pixel Value", fontsize=10)
        ax.set_title(f"Pixel ({i}, {j}) — {c} Bands", fontsize=11, fontweight="bold")
        ax.set_xlim(band_indices[0], band_indices[-1])
        ax.set_ylim(vmin, vmax)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.ticklabel_format(axis="y", style="scientific", scilimits=(0, 0))
        fig.tight_layout()

        save_path = os.path.join(pixel_img_dir, f"id_{gt_id}", f"pixel_{i:05d}_{j:05d}.png")
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        pbar.update(1)

pbar.close()

# ===== HTML 图册 =====
html_path = os.path.join(out_dir, "gallery.html")
id_label = {uid: ("Background" if uid == 0 else f"Class {uid}") for uid in unique_ids}

all_images = {}
for uid in unique_ids:
    subdir = os.path.join(pixel_img_dir, f"id_{uid}")
    if os.path.isdir(subdir):
        imgs = sorted(os.listdir(subdir))
        all_images[uid] = [(f"pixel_curves/id_{uid}/{f}", f) for f in imgs]

sections_html = "\n".join(
    f"  <div class='section' id='id-{uid}'>"
    f"<div class='section-title'>{id_label[uid]} (ID={uid}) — {len(all_images.get(uid, []))} pixels</div>"
    f"<div class='grid' id='grid-{uid}'></div></div>"
    for uid in unique_ids
)

toc_html = "\n".join(
    f"  <a href='#id-{uid}'>{id_label[uid]} ({len(all_images.get(uid, []))})</a>"
    for uid in unique_ids
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html lang='zh'>
<head><meta charset='UTF-8'>
<title>Pixel Curve Gallery — {os.path.basename(MAT_FILE)}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0d1117; color:#c9d1d9; font-family:'Segoe UI',sans-serif; }}
  .header {{ padding:24px 32px; border-bottom:1px solid #21262d; }}
  .header h1 {{ font-size:20px; color:#58a6ff; }}
  .header p {{ font-size:13px; color:#8b949e; margin-top:6px; }}
  .toc {{ padding:16px 32px; display:flex; gap:8px; flex-wrap:wrap; border-bottom:1px solid #21262d; }}
  .toc a {{ padding:6px 14px; border-radius:6px; background:#21262d; color:#c9d1d9; text-decoration:none; font-size:13px; border:1px solid #30363d; }}
  .section {{ padding:20px 32px; border-bottom:1px solid #21262d; }}
  .section-title {{ font-size:16px; font-weight:bold; margin-bottom:16px; color:#e6edf3; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; }}
  .card {{ background:#161b22; border:1px solid #30363d; border-radius:8px; overflow:hidden; transition:border-color .2s; }}
  .card:hover {{ border-color:#58a6ff; }}
  .card img {{ width:100%; height:90px; object-fit:cover; display:block; }}
  .card .label {{ padding:8px 12px; font-size:12px; color:#8b949e; }}
  .footer {{ padding:20px 32px; font-size:12px; color:#484f58; text-align:center; }}
</style>
</head>
<body>
<div class='header'>
  <h1>Pixel Curve Gallery — {os.path.basename(MAT_FILE)}</h1>
  <p>H={h}, W={w}, C={c} bands &nbsp;|&nbsp; GT IDs: {unique_ids}</p>
</div>
<div class='toc'>{toc_html}
</div>
{sections_html}
<script>
const images = {str({str(k): v for k, v in all_images.items()})};
Object.keys(images).forEach(id => {{
  const grid = document.getElementById('grid-' + id);
  images[id].forEach(([path, fname]) => {{
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `<img src='${{path}}' loading='lazy'><div class='label'>${{fname}}</div>`;
    grid.appendChild(card);
  }});
}});
</script>
<div class='footer'>Generated by pixel_curve_plotter.py — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
</body>
</html>""")
print(f"[图册]   {html_path}")

# ===== 统计 =====
print(f"\n{'='*60}\n各类别像素数量统计\n{'='*60}")
for uid in unique_ids:
    count = int(np.sum(gt_data == uid))
    pct = count / total_pixels * 100
    label = "背景" if uid == 0 else f"类别 {uid}"
    print(f"  ID={uid:3d}  {label:<12}  {count:>8}  pixels  ({pct:5.2f}%)")

print(f"\n{'='*60}\n完成！结果已保存至: {out_dir}")
print(f"  1. 00_overview.png         — 全局概览图")
print(f"  2. 01_mean_all.png        — 所有 ID 平均曲线合集")
print(f"  3. 01_mean_idNN.png       — 每个 ID 的平均曲线（各一张）")
print(f"  3. pixel_curves/id_N/     — 每个 ID 一个子文件夹")
print(f"  4. gallery.html            — HTML 图册（按 ID 分组）")
print(f"{'='*60}")
