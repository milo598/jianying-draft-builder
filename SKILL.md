---
name: jianying-draft-builder
description: 剪映专业版 11.x 草稿一键构建。把图片序列按指定时长、口播语音、BGM、SRT 字幕、转场和入场动画自动搭进剪映草稿，生成可编辑的剪辑工程。当用户要在剪映里批量排图、配音频字幕、做可精修的时间轴时使用。
version: 1.0.0
---

# JianYing Draft Builder

Use this skill when the user wants to build a JianYing Pro (剪映专业版) 11.x draft programmatically — laying out an image sequence on the timeline by exact durations, adding voiceover + BGM tracks, importing SRT subtitles, and applying transitions and entrance animations — without dragging clips by hand.

## 核心流程

1. 读 `config.json`（图片序列 + 时长 + 音频 + 字幕 + 转场 + 动画）。
2. 用 `ffmpeg` 把第一张图转成封面视频（`create` 命令需要一个视频素材起稿）。
3. 依次调用 `jianying-tool` CLI：
   - `create` 建竖屏/横屏草稿
   - `append-image` 逐张按 `target-start` + `duration` 排图
   - `append-audio` 加口播轨 + BGM 轨（音量、淡入淡出）
   - `subtitle` 导入 SRT
   - `transition` 给相邻片段加叠化
   - `animation` 给每页加轻微放大入场
4. `doctor` 自检，确认轨道、片段、素材引用完整。

## 运行

```bash
python scripts/build_draft.py examples/config.example.json
```

## 铁律

- **操作前必须关闭剪映**。剪映运行时会把草稿加密、占用文件，导致 `jianying-tool` 报
  `root and active timeline draft files differ` 或解密失败。
- 剪映 11.x 打开草稿后会把 `draft_content.json` 重新加密，属正常现象，不影响使用。
- `create` 需要 `--video`，脚本内部会用第一张图生成一个封面视频再调用。
- 素材路径在 config 里写相对路径（相对 config 文件所在目录）最稳妥。

## 依赖

- Python 3.10+
- `pip install jianying-tool imageio-ffmpeg`
- 剪映专业版 11.x（Windows）

## 自检

```bash
python -m jianying_tool.cli probe --json
```
