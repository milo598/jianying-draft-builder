# jianying-draft-builder v1.0.0

**剪映 (JianYing) 专业版 11.x 草稿一键构建 Skill。**  通过一份配置文件，把图片序列、口播语音、BGM、字幕、转场和入场动效自动搭进剪映草稿，生成可直接编辑的剪辑工程，不用手动拖时间轴。

## 功能特性

- **图片时序排布**  - 图片序列按指定时长排进视频轨
- **口播 + BGM**  - 音频各自成轨，支持音量与淡入淡出
- **字幕导入**  - SRT 一键进草稿，自动对齐
- **转场 / 动效**  - 页面间叠化转场，每页轻微放大入场
- **竖屏 / 横屏**  - 画布尺寸可配置
- **完整性自检**  - 构建后 doctor 检查轨道、片段、素材引用

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
