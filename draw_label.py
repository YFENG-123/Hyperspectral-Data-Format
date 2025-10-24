import matplotlib.pyplot as plt 
import numpy as np   
import scipy.io as sio
import json 
import cv2  

from matplotlib.path import Path

# 打开json文件
json_data = dict()
with open('C:\\Users\\zzh\\Desktop\\1.json', 'r') as f:
    json_data = json.load(f)
    print(json_data)

# 读取并显示图像
image_tif = cv2.imread("C:\\Users\\zzh\\Desktop\\1.tif")
plt.imshow(image_tif)

# 获取图像大小
height, width = image_tif.shape[:2]

# 创建图像大小的矩阵（以便存为mat）
image_mat = np.zeros((height, width), dtype=np.uint8)



# 绘制封闭多边形
for shape in json_data["shapes"]:

    x_coords = [point[0] for point in shape["points"]] + [shape["points"][0][0]]
    y_coords = [point[1] for point in shape["points"]] + [shape["points"][0][1]]
    plt.fill(x_coords, y_coords, facecolor='red', edgecolor='red', alpha=0.3, linewidth=1)

    # 创建多边形路径
    polygon_points = [(point[0], point[1]) for point in shape["points"]]
    polygon_path = Path(polygon_points)

    # 生成网格坐标点
    y_grid, x_grid = np.mgrid[0:height, 0:width]
    pixel_points = np.column_stack((x_grid.ravel(), y_grid.ravel()))
    
    # 检查每个像素点是否在多边形内
    inside_mask = polygon_path.contains_points(pixel_points)
    
    # 将一维掩码重塑为二维图像形状
    inside_mask_2d = inside_mask.reshape(height, width)
    
    # 直接修改image_mat矩阵中的值（使用多边形索引作为标签值）
    image_mat[inside_mask_2d] = 1


sio.savemat('labeled_image.mat', {'image_mat': image_mat})

plt.show()





