#使用BRIR和单通道语音来生成双耳语音信号
# /mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/brir_example.wav
# /mnt/nas1/project/dataset/urgent_2026_16KHz/clean/fileid_1.wav

import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

def render_binaural(brir_path, mono_path, output_path):
    """
    使用BRIR和单通道语音生成双耳语音信号
    
    Args:
        brir_path: BRIR文件路径（双通道wav，左右耳脉冲响应）
        mono_path: 单通道语音文件路径
        output_path: 输出双耳语音文件路径
    """
    # 读取BRIR（双通道：左耳和右耳的脉冲响应）
    brir, brir_sr = sf.read(brir_path)
    print(f"BRIR shape: {brir.shape}, sample rate: {brir_sr}")

    # 确保BRIR是双通道
    if brir.ndim == 1:
        raise ValueError("BRIR文件应为双通道（左耳/右耳），但读取到的是单通道")
    
    brir_left = brir[:, 0]
    brir_right = brir[:, 1]

    # 读取单通道语音
    mono, mono_sr = sf.read(mono_path)
    print(f"Mono speech shape: {mono.shape}, sample rate: {mono_sr}")

    # 如果语音是多通道，取第一个通道
    if mono.ndim > 1:
        mono = mono[:, 0]

    # 检查采样率是否一致，不一致则重采样单通道语音
    if mono_sr != brir_sr:
        print(f"采样率不一致: mono={mono_sr}, brir={brir_sr}，正在重采样...")
        import librosa
        mono = librosa.resample(mono, orig_sr=mono_sr, target_sr=brir_sr)
        mono_sr = brir_sr

    # 使用FFT卷积生成双耳信号
    binaural_left = fftconvolve(mono, brir_left, mode='full')
    binaural_right = fftconvolve(mono, brir_right, mode='full')

    # 合并为双通道
    binaural = np.stack([binaural_left, binaural_right], axis=-1)

    # 归一化，防止削波
    max_val = np.max(np.abs(binaural))
    if max_val > 0:
        binaural = binaural / max_val * 0.95

    # 保存输出
    sf.write(output_path, binaural, brir_sr)
    print(f"双耳语音已保存到: {output_path}")
    print(f"Output shape: {binaural.shape}, sample rate: {brir_sr}")
    print(f"Duration: {binaural.shape[0] / brir_sr:.2f}s")


if __name__ == "__main__":
    brir_path = "/mnt/nas1/project/dataset/brirs/05-office/pos00/az000_el-20_d1.50.wav"
    # /mnt/nas1/project/dataset/ARI_SOFA_HRTF/wavs/NH4/NH4_idx0390_az090_el-030_r1.20m.wav
    mono_path = "/mnt/nas1/project/dataset/urgent_2026_16KHz/clean/fileid_1.wav"
    output_path = "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/binaural_output.wav"

    render_binaural(brir_path, mono_path, output_path)