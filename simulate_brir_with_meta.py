import argparse
import json
import os

import numpy as np
import soundfile as sf

import simulator


def parse_float_list(value, expected_len):
    values = [float(x.strip()) for x in value.split(",")]
    if len(values) != expected_len:
        raise ValueError(
            f"Expected {expected_len} comma-separated values, got {len(values)}: {value}"
        )
    return values


def parse_int_list(value, expected_len):
    values = [int(x.strip()) for x in value.split(",")]
    if len(values) != expected_len:
        raise ValueError(
            f"Expected {expected_len} comma-separated values, got {len(values)}: {value}"
        )
    return values


def main():
    parser = argparse.ArgumentParser(
        description="Simulate one BRIR and save BRIR + metadata (geometry, RT60, DOA)."
    )
    parser.add_argument(
        "--room-materials",
        type=str,
        default="1,1,1,1,15,16",
        help="Material IDs for [x0, x1, y0, y1, floor, ceiling]",
    )
    parser.add_argument(
        "--room-dim-xyz",
        type=str,
        default="10,10,3",
        help="Room dimensions [X,Y,Z] in meters",
    )
    parser.add_argument(
        "--head-pos-xyz",
        type=str,
        default="5,5,1.5",
        help="Head position [X,Y,Z] in meters",
    )
    parser.add_argument("--head-azim", type=float, default=0.0, help="Head azimuth in degrees")
    parser.add_argument(
        "--src-azim", type=float, default=75.0, help="Source azimuth relative to head in degrees"
    )
    parser.add_argument(
        "--src-elev", type=float, default=0.0, help="Source elevation relative to head in degrees"
    )
    parser.add_argument("--src-dist", type=float, default=1.4, help="Source distance in meters")
    parser.add_argument("--sr", type=int, default=44100, help="Sampling rate in Hz")
    parser.add_argument("--dur", type=float, default=0.5, help="BRIR duration in seconds")
    parser.add_argument("--processes", type=int, default=8, help="Parallel worker processes")
    parser.add_argument(
        "--out-prefix",
        type=str,
        default="output/brir_example",
        help="Output prefix. Writes <prefix>.wav and <prefix>.meta.json",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict in-room validation for head/source positions",
    )

    args = parser.parse_args()

    room_materials = parse_int_list(args.room_materials, expected_len=6)
    room_dim_xyz = parse_float_list(args.room_dim_xyz, expected_len=3)
    head_pos_xyz = parse_float_list(args.head_pos_xyz, expected_len=3)

    brir, meta = simulator.get_brir_and_meta(
        room_materials=room_materials,
        room_dim_xyz=room_dim_xyz,
        head_pos_xyz=head_pos_xyz,
        head_azim=args.head_azim,
        src_azim=args.src_azim,
        src_elev=args.src_elev,
        src_dist=args.src_dist,
        sr=args.sr,
        dur=args.dur,
        processes=args.processes,
        strict=args.strict,
        verbose=1,
    )

    out_wav = f"{args.out_prefix}.wav"
    out_meta = f"{args.out_prefix}.meta.json"
    out_dir = os.path.dirname(out_wav)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    sf.write(out_wav, brir, args.sr)

    # Ensure metadata values are JSON serializable.
    meta_serializable = json.loads(json.dumps(meta, default=lambda o: float(o)))
    with open(out_meta, "w", encoding="utf-8") as f:
        json.dump(meta_serializable, f, indent=2, ensure_ascii=False)

    print(f"[saved] BRIR wav: {out_wav}")
    print(f"[saved] metadata: {out_meta}")
    print(f"[shape] brir: {brir.shape}")
    print(f"[meta] RT60(sabine-mid): {meta_serializable['rt60']['sabine']['rt60_mid_sec']:.3f} s")
    rt60_from_brir = meta_serializable["rt60"].get("from_brir", {}).get("rt60_from_brir_sec")
    print(f"[meta] RT60(from_brir): {rt60_from_brir}")
    print(
        "[meta] DOA(head): azim={:.1f} deg, elev={:.1f} deg".format(
            meta_serializable["doa"]["azim_deg_rel_head"],
            meta_serializable["doa"]["elev_deg_rel_head"],
        )
    )


if __name__ == "__main__":
    main()
