# CLAUDE.md — Mirror GUI 图片镜像工具

## 项目概述
图片水平镜像翻转工具，支持单张或批量处理。

## 技术栈
- Python 3.12+ / tkinter / Pillow

## 文件结构
```
mirror_gui.py       # 主程序
run_mirror.vbs      # 静默启动（自动探测 Python 路径）
debug_mirror.vbs    # 调试启动（带控制台）
```

## 功能要点
- 水平镜像翻转
- 单张 / 批量文件夹处理
- 输出文件自动添加 `_mirror` 后缀
- 进度条 + 日志
- 支持 JPG、PNG、WEBP、BMP、TIFF

## 规则
- 本项目较简单，暂无 exe 打包需求
