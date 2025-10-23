# 高光谱数据集格式化工具

## 运行环境
- Python >= 3.12

## 安装依赖
```
pip install -r requirements.txt
```

## 启动
```
python main.py
```

## 功能
- [x] 合并 **Labelme** 标注数据 
  - ``File -- Combine`` 选择需要合并的 **Json** 文件打开
  - 等待处理（程序阻塞）
  - 选择保存文件的位置，填写文件名保存合并后**Json** 文件
- [x] 统计 **Labelme** 数据标签数量
  - ``File -- Open`` 选择需要统计的 **Json** 文件打开
  - ``File -- Count`` 统计标签数量
- [x] 生成 **ID**
  - 统计标签数量后后 ``File -- Generate ID`` 
- [x] 图像生成 **MAT** 文件
  - ``File -- Open_tif`` 选择 **TIF** 文件打开
  - ``File -- Save_mat`` 选择保存文件的位置，填写文件名保存 **MAT** 文

- [ ] *绘制 **Labelme** 数据 **(开发中)***
  - ``File -- Open_tif`` 选择 **TIF** 文件打开
  - ``File -- Open`` 选择 **Json** 文件打开
  - ``File -- Draw`` 绘制 **Labelme** 数据 **(开发中)**
件
- [ ] *框选区域裁切 **(开发中)***
- [ ] ***Labelme** 数据生成**MAT** 文件 **(开发中)***

