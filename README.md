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
- [x] 合并 **Labelme** 标注数据 
  - ``File -- Combine`` 选择需要合并的 **Json** 文件打开
  - 等待处理（程序阻塞）
  - 选择保存文件的位置，填写文件名保存合并后**Json** 文件
- [x] 统计 **Labelme** 数据标签数量
  - ``File -- Open`` 选择需要统计的 **Json** 文件打开
  - ``File -- Count`` 统计标签数量
- [x] 生成 **ID**
  - 统计标签数量后后 ``File -- Generate ID`` 
- [ ] 图像生成 **MAT** 文件
  - ``File -- Open_tif`` 选择 **TIF** 文件打开
  - ``File -- Save_mat`` 选择保存文件的位置，填写文件名保存 **MAT** 文

- [ ] *绘制 **Labelme** 数据 **(开发中)***
  - ``File -- Open_tif`` 选择 **TIF** 文件打开
  - ``File -- Open`` 选择 **Json** 文件打开
  - ``File -- Draw`` 绘制 **Labelme** 数据 **(开发中)**
件
- [ ] *框选区域裁切 **(开发中)***
- [ ] ***Labelme** 数据生成**MAT** 文件 **(开发中)***





# 贡献指南

**感谢你为本项目项目做出贡献!!！**

## 推荐开发工具

- [VsCode](https://code.visualstudio.com/)
- [Ruff 插件](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [git-commit-plugin](https://marketplace.visualstudio.com/items?itemName=redjue.git-commit-plugin)

## 项目分支

- `main` 主分支（生产环境）

  用于生产环境的线上版本代码。不允许直接向 `main` 分支提交代码，需要通过 Pull Request 从 `dev` 分支合并代码。（此操作仅由项目管理员完成）

- `dev` 开发分支（测试环境）

  用于测试新功能和最新的 bug 修改。不允许直接向 `dev` 分支提交代码，需要通过 Pull Request 从 其他 分支合并代码。

## 贡献

1. 准备新分支

   在本地拉取最新的项目代码/同步到最新的项目代码，切换到 `dev` 分支，新建一个分支 `example`。

   ```bash
   # 同步远端仓库最新进度
   git fetch
   # 切换到 dev 分支
   git checkout dev
   # 拉取最新代码
   git pull
   # 新建分支
   git checkout -b examplebranch
   ```

2. 修改代码并提交新分支

   在自测完成后，请提交代码。**请注意，请你再次确认你的代码已经通过了你的本地测试。**

   ```bash
   # 添加修改
   git add .
   # 提交修改
   git commit -m "message"
   # 推送到远程仓库
   git push origin examplebranch
   ```

   请在提交信息 `message` 处填写你本次对代码修改的内容。

3. 提交 Pull Request

   提交 Pull Request 从 `examplbranch` 到 `main` 分支。在 Pull Request 中，请确保你的代码通过了所有的测试，没有任何冲突。在 Pull Request 中，请详细描述你的修改，以及你的修改如何解决了问题。

4. 合并 Pull Request

   当你的 Pull Request 被授权后，你可以将你的代码合并到 `main` 分支。在合并之前，请确保你的代码没有任何冲突，也没有任何测试失败。合并完成后，你可以安全地删除分支 `examplebranch`。

   **请注意：严格禁止直接 push 到 `main` 分支**
