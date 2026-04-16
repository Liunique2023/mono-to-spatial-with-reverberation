import os
import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve


def load_audio(path, target_sr=None):
    """加载音频文件，返回 (data, sr)"""
    data, sr = sf.read(path, dtype='float64')
    if target_sr is not None and sr != target_sr:
        import librosa
        data = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
        sr = target_sr
    return data, sr


def convolve_rir(mono_signal, rir_signal):
    """将单通道语音与 RIR 卷积，模拟房间混响（单通道输出）"""
    if rir_signal.ndim > 1:
        rir_signal = rir_signal[:, 0]  # 取第一个通道
    reverbed = fftconvolve(mono_signal, rir_signal, mode='full')
    # 归一化防止溢出
    peak = np.max(np.abs(reverbed))
    if peak > 0:
        reverbed = reverbed / peak * np.max(np.abs(mono_signal))
    return reverbed


def convolve_hrtf(mono_signal, hrtf_stereo):
    """将单通道语音与双耳 HRTF 卷积，生成双耳立体声输出"""
    if hrtf_stereo.ndim == 1:
        # 如果 HRTF 是单通道，左右耳用同一个
        hrtf_L = hrtf_stereo
        hrtf_R = hrtf_stereo
    else:
        hrtf_L = hrtf_stereo[:, 0]
        hrtf_R = hrtf_stereo[:, 1]

    out_L = fftconvolve(mono_signal, hrtf_L, mode='full')
    out_R = fftconvolve(mono_signal, hrtf_R, mode='full')

    # 归一化
    peak = max(np.max(np.abs(out_L)), np.max(np.abs(out_R)))
    if peak > 0:
        scale = np.max(np.abs(mono_signal)) / peak
        out_L *= scale
        out_R *= scale

    binaural = np.stack([out_L, out_R], axis=-1)
    return binaural


def rir_hrtf_cascade(mono_path, rir_path, hrtf_path, output_path, target_sr=16000):
    """
    级联处理：单通道语音 -> RIR卷积(混响) -> HRTF卷积(空间化) -> 双耳输出
    """
    # 1. 加载单通道干净语音
    mono, sr = load_audio(mono_path, target_sr=target_sr)
    if mono.ndim > 1:
        mono = mono[:, 0]
    print(f"[INFO] Loaded mono speech: {mono_path}, sr={sr}, len={len(mono)}")

    # 2. 加载 RIR 并卷积
    rir, rir_sr = load_audio(rir_path, target_sr=target_sr)
    reverbed = convolve_rir(mono, rir)
    print(f"[INFO] Applied RIR: {rir_path}, rir_sr={rir_sr}, rir_len={len(rir)}")

    # 3. 加载 HRTF 并卷积
    hrtf, hrtf_sr = load_audio(hrtf_path, target_sr=target_sr)
    binaural = convolve_hrtf(reverbed, hrtf)
    print(f"[INFO] Applied HRTF: {hrtf_path}, hrtf_sr={hrtf_sr}, hrtf_len={len(hrtf)}")

    # 4. 保存双耳输出
    sf.write(output_path, binaural, sr)
    print(f"[INFO] Saved binaural output: {output_path}, shape={binaural.shape}")

    return binaural, sr


if __name__ == "__main__":
    # ========== 配置路径 ==========
    mono_path = "/mnt/nas1/project/dataset/urgent_2026_16KHz/clean/fileid_1.wav"

    # 四组不同的 RIR + HRTF 组合，生成四组双耳语音
    configs = [
        {
            "rir_path": "/mnt/nas1/project/urgent2026_challenge_track1/download/RIR/datasets_fullband/impulse_responses/SLR26/simulated_rirs_48k/largeroom/Room001/Room001-00001.wav",
            "hrtf_path": "/mnt/nas1/project/dataset/ARI_SOFA_HRTF/wavs/NH4/NH4_idx0390_az090_el-030_r1.20m.wav",
            "output_path": "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/binaural_group1.wav",
            "desc": "大房间 + HRTF(az090, el-030)",
        },
        {
            "rir_path": "/mnt/nas1/project/urgent2026_challenge_track1/download/RIR/datasets_fullband/impulse_responses/SLR26/simulated_rirs_48k/smallroom/Room001/Room001-00001.wav",
            "hrtf_path": "/mnt/nas1/project/dataset/ARI_SOFA_HRTF/wavs/NH4/NH4_idx0390_az090_el-030_r1.20m.wav",
            "output_path": "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/binaural_group2.wav",
            "desc": "小房间 + HRTF(az090, el-030)",
        },
        {
            "rir_path": "/mnt/nas1/project/urgent2026_challenge_track1/download/RIR/datasets_fullband/impulse_responses/SLR26/simulated_rirs_48k/largeroom/Room001/Room001-00001.wav",
            "hrtf_path": "/mnt/nas1/project/dataset/ARI_SOFA_HRTF/wavs/NH2/NH2_idx0006_az000_el+000_r1.20m.wav",
            "output_path": "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/binaural_group3.wav",
            "desc": "大房间 + HRTF(另一方向，请替换路径)",
        },
        {
            "rir_path": "/mnt/nas1/project/urgent2026_challenge_track1/download/RIR/datasets_fullband/impulse_responses/SLR26/simulated_rirs_48k/smallroom/Room001/Room001-00001.wav",
            "hrtf_path": "/mnt/nas1/project/dataset/ARI_SOFA_HRTF/wavs/NH2/NH2_idx0006_az000_el+000_r1.20m.wav",
            "output_path": "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output/binaural_group4.wav",
            "desc": "小房间 + HRTF(另一方向，请替换路径)",
        },
    ]

    target_sr = 16000
    output_dir = "/mnt/nas1/project/spatial_audio/virtual_acoustic_room-main/output"
    os.makedirs(output_dir, exist_ok=True)

    for i, cfg in enumerate(configs):
        print(f"\n{'='*60}")
        print(f"[Group {i+1}] {cfg['desc']}")
        print(f"{'='*60}")
        rir_hrtf_cascade(
            mono_path=mono_path,
            rir_path=cfg["rir_path"],
            hrtf_path=cfg["hrtf_path"],
            output_path=cfg["output_path"],
            target_sr=target_sr,
        )

    print("\n[DONE] 四组双耳空间音频生成完毕！")