#!/usr/bin/env python3
"""
render_all_scenes.py
使用 brirs_simple 目录下的 BRIR 与单通道语音卷积，生成双耳空间音频。

使用方法:
  cd /mnt/nas1/project/spatial_audio/virtual_acoustic_room-main
  python render_all_scenes.py
"""

import os
import glob
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve
import librosa

MONO_PATH = "/mnt/nas1/project/dataset/urgent_2026_16KHz/clean/fileid_1.wav"
BRIR_DIR = "/mnt/nas1/project/dataset/brirs_simple"
OUTPUT_DIR = "output/rendered"

# (场景目录名, 方位角前缀, 中文描述)
# az000_el+00 = 正前方(0°), az090_el+00 = 左方(90°)
SCENES = [
    ("01-anechoic_chamber",   "az000_el+00", "消声室-前方"),
    ("01-anechoic_chamber",   "az090_el+00", "消声室-左方"),
    ("02-recording_studio",   "az000_el+00", "录音棚-前方"),
    ("02-recording_studio",   "az090_el+00", "录音棚-左方"),
    ("03-car_interior",       "az000_el+00", "车内-前方"),
    ("03-car_interior",       "az090_el+00", "车内-左方"),
    ("05-office",             "az000_el+00", "办公室-前方"),
    ("05-office",             "az090_el+00", "办公室-左方"),
    ("06-living_room",        "az000_el+00", "客厅-前方"),
    ("06-living_room",        "az090_el+00", "客厅-左方"),
    ("09-small_concert_hall", "az000_el+00", "小音乐厅-前方"),
    ("09-small_concert_hall", "az090_el+00", "小音乐厅-左方"),
    ("10-open_office",        "az000_el+00", "开放办公区-前方"),
    ("10-open_office",        "az090_el+00", "开放办公区-左方"),
    ("11-bathroom_tile",      "az000_el+00", "瓷砖浴室-前方"),
    ("11-bathroom_tile",      "az090_el+00", "瓷砖浴室-左方"),
    ("12-medium_theater",     "az000_el+00", "中型剧院-前方"),
    ("12-medium_theater",     "az090_el+00", "中型剧院-左方"),
    ("13-indoor_gymnasium",   "az000_el+00", "室内体育馆-前方"),
    ("13-indoor_gymnasium",   "az090_el+00", "室内体育馆-左方"),
    ("19-outdoor_open",       "az000_el+00", "室外开阔-前方"),
    ("19-outdoor_open",       "az090_el+00", "室外开阔-左方"),
    ("21-forest",             "az000_el+00", "森林-前方"),
    ("21-forest",             "az090_el+00", "森林-左方"),
]


def find_brir_file(scene_dir, az_prefix):
    """根据方位角前缀在 pos00 目录下查找第一个匹配的 BRIR 文件"""
    pattern = os.path.join(BRIR_DIR, scene_dir, "pos00", f"{az_prefix}_*.wav")
    matches = sorted(glob.glob(pattern))
    if matches:
        return matches[0]
    return None


def render_binaural(mono, mono_sr, brir_path):
    brir, brir_sr = sf.read(brir_path)

    if brir.ndim == 1:
        raise ValueError(f"BRIR应为双通道，但 {brir_path} 是单通道")

    brir_left = brir[:, 0]
    brir_right = brir[:, 1]

    if mono_sr != brir_sr:
        mono_resampled = librosa.resample(mono, orig_sr=mono_sr, target_sr=brir_sr)
    else:
        mono_resampled = mono

    binaural_left = fftconvolve(mono_resampled, brir_left, mode='full')
    binaural_right = fftconvolve(mono_resampled, brir_right, mode='full')

    binaural = np.stack([binaural_left, binaural_right], axis=-1)

    max_val = np.max(np.abs(binaural))
    if max_val > 0:
        binaural = binaural / max_val * 0.95

    return binaural, brir_sr


def main():
    print(f"读取单通道语音: {MONO_PATH}")
    mono, mono_sr = sf.read(MONO_PATH)
    if mono.ndim > 1:
        mono = mono[:, 0]
    print(f"  采样率: {mono_sr} Hz, 时长: {len(mono)/mono_sr:.2f}s")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"\n{'='*60}")
    print(f" 开始渲染 {len(SCENES)} 个场景")
    print(f"{'='*60}")

    for i, (scene_dir, az_prefix, scene_name) in enumerate(SCENES, 1):
        brir_path = find_brir_file(scene_dir, az_prefix)

        if brir_path is None:
            search_pattern = os.path.join(BRIR_DIR, scene_dir, "pos00", f"{az_prefix}_*.wav")
            print(f"\n[{i}/{len(SCENES)}] ⚠ 跳过 {scene_name}: 未找到匹配文件 ({search_pattern})")
            continue

        print(f"\n[{i}/{len(SCENES)}] 渲染: {scene_name}")
        print(f"  BRIR: {brir_path}")

        binaural, out_sr = render_binaural(mono, mono_sr, brir_path)

        out_subdir = os.path.join(OUTPUT_DIR, scene_dir)
        os.makedirs(out_subdir, exist_ok=True)

        brir_basename = os.path.splitext(os.path.basename(brir_path))[0]
        out_path = os.path.join(out_subdir, f"{brir_basename}_binaural.wav")

        sf.write(out_path, binaural, out_sr)
        print(f"  输出: {out_path}")
        print(f"  采样率: {out_sr} Hz, 时长: {binaural.shape[0]/out_sr:.2f}s, shape: {binaural.shape}")

    print(f"\n{'='*60}")
    print(f" 全部完成! 输出目录: {OUTPUT_DIR}/")
    print(f"{'='*60}\n")

    print("输出文件列表:")
    for root, dirs, files in sorted(os.walk(OUTPUT_DIR)):
        for f in sorted(files):
            if f.endswith('.wav'):
                fpath = os.path.join(root, f)
                info = sf.info(fpath)
                print(f"  {fpath}  ({info.duration:.2f}s, {info.channels}ch, {info.samplerate}Hz)")


if __name__ == "__main__":
    main()