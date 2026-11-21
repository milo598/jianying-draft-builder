#!/usr/bin/env python3
"""剪映专业版 11.x 草稿一键构建器。

用法:
    python build_draft.py <config.json>

config.json 结构见 examples/config.example.json。
"""

import json
import shutil
import subprocess
import sys
import os
from pathlib import Path

DEFAULT_DRAFT_ROOT = os.path.join(
    os.environ.get("LOCALAPPDATA", ""),
    "JianyingPro", "User Data", "Projects", "com.lveditor.draft",
)


def get_ffmpeg() -> str:
    """优先用 imageio_ffmpeg 自带的 ffmpeg，否则退回 PATH 里的 ffmpeg。"""
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.isfile(exe):
            return exe
    except Exception:
        pass
    return "ffmpeg"


def run_cli(args):
    """调用 jianying-tool CLI，失败直接抛异常。"""
    cmd = [sys.executable, "-m", "jianying_tool.cli"] + [str(a) for a in args]
    label = " ".join(str(a) for a in args[:2])
    print(f"  -> {label}")
    subprocess.run(cmd, check=True)


def resolve(path, base: Path) -> str:
    """相对路径按 config 文件所在目录解析。"""
    p = Path(path)
    return str(p if p.is_absolute() else (base / p).resolve())


def make_cover_video(image: str, duration: int, out: Path, width: int, height: int):
    ffmpeg = get_ffmpeg()
    print(f"生成封面视频 {duration}s ...")
    subprocess.run([
        ffmpeg, "-y", "-loop", "1", "-i", image,
        "-t", str(duration), "-r", "30",
        "-vf", f"scale={width}:{height},setsar=1",
        "-pix_fmt", "yuv420p", "-c:v", "libx264",
        str(out),
    ], check=True, capture_output=True)


def build(config_path: str):
    cfg_path = Path(config_path).resolve()
    base = cfg_path.parent
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    draft_name = cfg["draft_name"]
    width = int(cfg.get("width", 1080))
    height = int(cfg.get("height", 1920))
    draft_root = cfg.get("draft_root") or DEFAULT_DRAFT_ROOT

    images = cfg.get("images") or []
    if not images:
        raise SystemExit("配置里 images 不能为空")

    cover_dur = int(images[0].get("duration", 3))
    first_img = resolve(images[0]["file"], base)

    # 1. 第一张图 -> 封面视频（create 需要一个视频素材起稿）
    cover_mp4 = base / f".cover_{draft_name}.mp4"
    make_cover_video(first_img, cover_dur, cover_mp4, width, height)

    try:
        # 2. 删除同名旧草稿，避免剪映索引冲突
        old = Path(draft_root) / draft_name
        if old.is_dir():
            print("删除旧草稿:", old)
            shutil.rmtree(old)

        # 3. 建草稿（封面视频取前 N 秒）
        print(f"创建草稿: {draft_name} ({width}x{height})")
        run_cli(["create", "--name", draft_name, "--video", str(cover_mp4),
                 "--duration", str(cover_dur), "--width", str(width), "--height", str(height)])

        # 4. 其余图片按 target-start 顺序排进视频轨
        start = cover_dur
        for item in images[1:]:
            img = resolve(item["file"], base)
            dur = int(item["duration"])
            print(f"追加图片 {Path(item['file']).name}  start={start}s dur={dur}s")
            run_cli(["append-image", "--draft", draft_name, "--image", img,
                     "--track", "main_video", "--target-start", str(start),
                     "--duration", str(dur)])
            start += dur

        # 5. 口播 + BGM
        voice = cfg.get("voice")
        if voice:
            print("追加口播语音轨")
            run_cli(["append-audio", "--draft", draft_name,
                     "--audio", resolve(voice["file"], base),
                     "--track", "口播",
                     "--volume", str(voice.get("volume", 1.0)),
                     "--fade-in", str(voice.get("fade_in", 0.3)),
                     "--fade-out", str(voice.get("fade_out", 0.5))])

        bgm = cfg.get("bgm")
        if bgm:
            print("追加 BGM 轨")
            run_cli(["append-audio", "--draft", draft_name,
                     "--audio", resolve(bgm["file"], base),
                     "--track", "BGM",
                     "--volume", str(bgm.get("volume", 0.13)),
                     "--fade-in", str(bgm.get("fade_in", 1.5)),
                     "--fade-out", str(bgm.get("fade_out", 1.5))])

        # 6. 字幕
        sub = cfg.get("subtitle")
        if sub:
            print("导入 SRT 字幕")
            run_cli(["subtitle", "--draft", draft_name, "--srt", resolve(sub, base)])

        # 7. 转场（相邻片段之间）
        tr = cfg.get("transition")
        if tr:
            for i in range(len(images) - 1):
                run_cli(["transition", "--draft", draft_name, "--track", "main_video",
                         "--segment", str(i), "--name", tr.get("name", "叠化"),
                         "--duration", str(tr.get("duration", 0.5))])

        # 8. 入场动效（每页）
        an = cfg.get("animation")
        if an:
            for i in range(len(images)):
                run_cli(["animation", "--draft", draft_name, "--track", "main_video",
                         "--segment", str(i), "--kind", an.get("kind", "in"),
                         "--name", an.get("name", "轻微放大"),
                         "--duration", str(an.get("duration", 1.0))])

        # 9. 完整性检查
        print("完整性检查 ...")
        run_cli(["doctor", str(Path(draft_root) / draft_name)])
    finally:
        # 清理临时封面视频
        cover_mp4.unlink(missing_ok=True)

    print(f"\n完成！打开剪映，草稿列表里找「{draft_name}」。")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1])
