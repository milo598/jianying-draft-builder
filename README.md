# jianying-draft-builder v1.0.0

**剪映 (JianYing) 专业版 11.x 草稿一键构建 Skill。**  通过一份配置文件，把图片序列、口播语音、BGM、字幕、转场和入场动效自动搭进剪映草稿，生成可直接编辑的剪辑工程，不用手动拖时间轴。

## 功能特性

- **一键排图**  - 图片序列按指定时长自动排进时间轴，不用手动拖拽
- **音频自动成轨**  - 口播语音、BGM 各自成轨，音量、淡入淡出可调
- **字幕一键导入**  - SRT 直接进草稿，逐句对齐口播卡点
- **转场 / 动效**  - 页面间叠化转场，每页轻微放大入场，静态图也有呼吸感
- **竖屏 / 横屏自适应**  - 画布尺寸可配，竖屏 1080×1920 直接出抖音版
- **可编辑工程**  - 结果落在剪映草稿，时间轴可拖、可改、可加特效
- **构建自检**  - 完成后 doctor 检查轨道、片段、素材引用，零错误才交付
- **配置驱动**  - 改一个 JSON 就能复用，批量出片不用重写脚本

## 支持环境

| 平台 | 状态 | 说明 |
|---|---|---|
| Windows | ✅ | 完全支持，剪映专业版 11.x（实测 11.8） |
| macOS | ❌ | 未支持（底层依赖 Windows 的 videoeditor.dll） |

## 安装

复制以下命令发给 AI Agent：

```
帮我安装 jianying-draft-builder skill：
cd <workspace>/skills && git clone https://github.com/WUCEYWE/jianying-draft-builder.git && cd jianying-draft-builder && pip install -r requirements.txt
```

装完自检：

```
python -m jianying_tool.cli probe --json
```

## 使用

1. 复制 `examples/config.example.json`，改成自己的图片、时长、音频、字幕。
2. **先彻底关闭剪映**（否则草稿会被加密占用，写入失败）。
3. 运行：

```
python scripts/build_draft.py my-config.json
```

4. 打开剪映，草稿列表里找 `draft_name` 对应的草稿，点进去就是完整时间轴。

## 依赖要求

- Python 3.10+
- 剪映专业版 11.x（工具通过其自带 videoeditor.dll 读写草稿）
- ffmpeg（封面视频生成，imageio-ffmpeg 自动提供）

## 相关链接

- [SKILL.md](SKILL.md) - AI 说明书
- [jianying-tool](https://pypi.org/project/jianying-tool/) - 底层草稿读写库
