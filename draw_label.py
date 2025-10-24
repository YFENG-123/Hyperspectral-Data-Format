import matplotlib.pyplot as plt 
import numpy as np   
import scipy.io as sio
import json 
import cv2  

from matplotlib.path import Path

# 打开json文件
json_data = dict()
with open("D:\\Users\\YFENG\\Desktop\\20251013GGPBIL.json", 'r') as f:
    json_data = json.load(f)

# 读取并显示图像
image_tif = cv2.imread("D:\\Users\\YFENG\\Desktop\\20251013GGPBIL.tif")
plt.imshow(image_tif)

# 获取图像大小
height, width = image_tif.shape[:2]

# 创建图像大小的矩阵（以便存为mat）
image_mat = np.zeros((height, width), dtype=np.uint8)

i = 0
# 绘制封闭多边形
for shape in json_data["shapes"]:
    print(i)
    i += 1

    x_coords = [point[0] for point in shape["points"]] 
    y_coords = [point[1] for point in shape["points"]] 
    plt.fill(x_coords + [shape["points"][0][0]], y_coords + [shape["points"][0][1]], facecolor='red', edgecolor='red', alpha=0.3, linewidth=1)

    # 创建多边形路径
    polygon_points = [(point[0], point[1]) for point in shape["points"]]
    polygon_path = Path(polygon_points)

    # 计算多边形的边界框
    min_x = max(int(min(x_coords)), 0)
    min_y = max(int(min(y_coords)), 0)
    max_x = min(int(max(x_coords)), width)
    max_y = min(int(max(y_coords)), height)

    # 只在多边形周围的区域内生成网格点
    y_grid_roi, x_grid_roi = np.mgrid[min_y:max_y, min_x:max_x]
    pixel_points_roi = np.column_stack((x_grid_roi.ravel(), y_grid_roi.ravel()))

    # 检查ROI内每个像素点是否在多边形内
    inside_mask = polygon_path.contains_points(pixel_points_roi)
    
    # 将一维掩码重塑为二维ROI形状
    inside_mask_2d = inside_mask.reshape(y_grid_roi.shape)
    
    # 只更新ROI区域内的image_mat矩阵
    image_mat[min_y:max_y, min_x:max_x][inside_mask_2d] = 1 


sio.savemat('labeled_image.mat', {'image_mat': image_mat})

plt.show()





