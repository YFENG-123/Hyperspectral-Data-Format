# 高光谱数据集格式化工具

## 运行环境
- Python >= 3.12

## 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 启动
```bash
python app/app.py
```

## 功能
- [x] 打开 **JSON** 文件
  - ``Json -- Open`` 选择需要打开的 **Json** 文件
- [x] 合并 **Labelme** 标注数据 
  - ``Json -- Combine`` 选择需要合并的 **Json** 文件打开
  - 等待处理（程序阻塞）
  - 选择保存文件的位置，填写文件名保存合并后的**Json** 文件
- [x] 统计 **Labelme** 数据标签数量
  - ``Json -- Open`` 选择需要统计的 **Json** 文件打开
  - ``Json -- Count`` 统计标签数量
- [x] 生成**Labelme** 数据标签ID
  - ``Json -- Open`` 选择需要统计ID的 **Json** 文件打开
  - ``Json -- Id``  统计标签数量后生成标签 ID
- [x] **Labelme** 数据转换为 **TIF** 文件
  - ``Json -- Open`` 选择需要转换的 **Json** 文件打开
  - ``Json -- Convert_to_tif`` 将标注数据转换为 **TIF** 图像格式
  - 等待处理（程序阻塞）
  - 选择保存文件的位置，填写文件名保存转换后的**TIF** 格式文件
- [x] 打开 **MAT** 文件
  - ``Mat -- Open`` 选择需要打开的 **MAT** 文件
- [x] 打开 **TIF** 文件
  - ``TIF -- Open`` 选择需要打开的 **TIF** 文件
- [x] 保存 **TIF** 文件
  - ``TIF -- Save_tif`` 选择保存文件的位置，填写文件名保存 **TIF** 文件
- [x] 打开 **HDR** 文件
  - ``HDR -- Open`` 选择需要打开的 **HDR** 文件
- [x] 替换**Labelme** 数据标签 
  - ``Json -- Open`` 选择需要替换标签的 **Json** 文件打开
  - ``Json -- Replace_label`` 输入原始标签和新标签进行替换 
  - 选择是否保存修改后的文件
- [x] 删除**Labelme** 数据标签
  - ``Json -- Open`` 选择需要删除标签的 **Json** 文件打开
  - ``Json -- Delete_label`` 删除指定标签的标注
  - 保存修改后的 **Json** 文件
- [x] 绘制 **Labelme** 数据
  - ``TIF -- Open`` 选择 **TIF** 文件打开
  - ``Json -- Open`` 选择 **Json** 文件打开
  - ``Json -- Id`` 生成标签 ID
  - ``TIF -- Draw_label`` 在 **TIF** 图像上绘制 **Labelme** 标注数据
- [ ] **HDR** 转换为 **MAT** 文件 ***(修复中)***
  - ``HDR -- Open`` 选择需要转换的 **HDR** 文件打开
  - ``HDR -- Convert_to_mat`` 将 **HDR** 高光谱数据转换为 **MAT** 格式
  - 选择保存文件的位置，填写文件名保存 **MAT** 文件
- [ ] **HDR** 裁剪并转换为 **MAT** 文件 ***(开发中)***
  - ``HDR -- Open`` 选择需要转换的 **HDR** 文件打开
  - ``HDR -- Convert_to_mat_resize`` 指定裁剪区域坐标，将裁剪后的 **HDR** 数据转换为 **MAT** 格式
  - 自动保存为 **MAT** 文件
- [ ] 图像生成 **MAT** 文件 ***(修复中)***
  - ``Mat -- Save_mat`` 选择保存文件的位置，填写文件名保存 **MAT** 文件



# 贡献指南

**感谢你为本项目做出贡献!!！**

## 推荐开发工具

- [VsCode](https://code.visualstudio.com/)
- [Ruff 插件](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [git-commit-plugin](https://marketplace.visualstudio.com/items?itemName=redjue.git-commit-plugin)

## 项目分支

- `main` 主分支（生产环境）

  用于生产环境的线上版本代码。不允许直接向 `main` 分支提交代码，需要通过 Pull Request 从 `dev` 分支合并代码。（此操作仅由项目管理员完成）

- `dev` 开发分支（测试环境）

  用于测试新功能和最新的 bug 修改。不允许直接向 `dev` 分支提交代码，需要通过 Pull Request 从 其他 分支合并代码。

## 贡献流程

1. 克隆项目

   使用 git 工具克隆项目

   ```bash
   git clone https://github.com/your-username/your-project.git
   ```

2. 新建分支

   切换到 `dev` 分支，在本地拉取最新的项目代码/同步到最新的项目代码，新建一个分支 `example`。

   ```bash
   # 切换到 dev 分支
   git checkout dev
   # 拉取最新代码
   git pull
   # 新建分支
   git checkout -b feat/[issue id]
   ```

3. 修改代码并提交新分支

   在自测完成后，请提交代码。**请注意，请你再次确认你的代码已经通过了你的本地测试。**

   ```bash
   # 添加修改
   git add .
   # 提交修改
   git commit -m "message"
   # 推送到远程仓库
   git push origin feat/[issue id]
   ```

   请在提交信息 `message` 处填写你本次对代码修改的内容, 建议使用git-commit-plugin插件生成提交信息。

4. 提交 Pull Request

   提交 Pull Request 从 `feat/[issue id]` 到 `dev` 分支。在 Pull Request 中，请确保你的代码通过了所有的测试，没有任何冲突。在 Pull Request 中，请详细描述你的修改，以及你的修改如何解决了问题。

   **请注意：严格禁止直接 push 到 `main` 分支**
