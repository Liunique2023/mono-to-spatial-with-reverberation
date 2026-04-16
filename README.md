## Python virtual acoustic room simulator

This virtual acoustic room simulator uses the [Image-Source Method](https://www.mathworks.com/help/audio/ug/room-impulse-response-simulation-with-image-source-method-and-hrtf-interpolation.html#mw_rtc_RoomImpulseResponseImageSourceExample_M_FDE78C42) to render binaural room impulse responses (BRIRs) for spatializing audio in simple "shoebox" (cuboid) rooms. This is a Python port of [MATLAB code](src) by Mike O'Connell and Jay Desloge. We used this Python version to generate a large set of BRIRs for training [deep neural network models of human sound localization](https://doi.org/10.1038/s41467-024-54700-5).


### Requirements

- The Python implementation (`simulator.py`) requires only: `numpy`, `pandas`, `scipy`, `soundfile`

- The Python interface for calling the MATLAB implementation (`simulator_matlab.py`) requires the [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html)


### Conventions

- The `room_dim_xyz` argument specifies the `[X, Y, Z]` dimensions of a room with one corner at the origin.
- The `x-y` plane with `z=0` corresponds to the room's floor and `z=Z` corresponds to the room's ceiling.
- The `room_materials` argument is an ordered list of 6 integers corresponding to 4 walls, a floor, and a ceiling: `[x=0 wall, x=X wall, y=0 wall, y=Y wall, z=0 floor, z=Z ceiling]`. The integers correspond to materials defined in [`materials_original.csv`](materials_original.csv).
- 0 degrees azimuth is defined as parallel to a vector along the x-axis: `[1, 0, 0]`.
- **Positive azimuths indicate counter-clockwise rotation away from the x-axis in the `x-y` plane**. Note this azimuth convention is opposite to that used by Gardner & Martin to label the KEMAR HRTFs. The `simulator.get_brir` function handles this mismatch internally. When using the function, a source azimuth of +90 degrees is to the listener's left and -90 degrees is to the listener's right.
- Positive elevations indicate upward rotation away from the floor (`z=0` plane).


### Example usage

```
import simulator

room_materials = [1, 1, 1, 1, 15, 16]
room_dim_xyz = [10.0, 10.0, 3.0]  # X, Y, and Z dimensions of room in m
head_pos_xyz = [5.0, 5.0, 2.0]  # X, Y, and Z coordinates of head in m
head_azim = 0  # Head azimuth in degrees
src_azim = 75  # Source azimuth in degrees
src_elev = 0  # Source elevation in degrees
src_dist = 1.4  # Source distance in m

sr = 44100  # Sampling rate in Hz to match KEMAR HRTFs
dur = 0.5  # Duration of BRIR in seconds

brir = simulator.get_brir(
    room_materials=room_materials,
    room_dim_xyz=room_dim_xyz,
    head_pos_xyz=head_pos_xyz,
    head_azim=head_azim,
    src_azim=src_azim,
    src_elev=src_elev,
    src_dist=src_dist,
    sr=sr,
    dur=dur,
)
print(brir.shape)  # --> [22050 timesteps, 2 channels = left and right ear]
```


### Simulate one BRIR and save metadata (geometry, RT60, DOA)

Use the helper script below to generate one BRIR and save both:

- `<prefix>.wav`: binaural impulse response
- `<prefix>.meta.json`: metadata including room geometry, source/listener pose, DOA, and RT60 estimates

```
python simulate_brir_with_meta.py \
    --room-materials 1,1,1,1,15,16 \
    --room-dim-xyz 10,10,3 \
    --head-pos-xyz 5,5,1.5 \
    --head-azim 0 \
    --src-azim 75 \
    --src-elev 0 \
    --src-dist 1.4 \
    --sr 44100 \
    --dur 0.5 \
    --out-prefix output/brir_example
```

The generated metadata JSON includes:

- Room geometry: dimensions, volume, and surface area
- Source/listener geometry: xyz positions and source distance
- DOA: azimuth/elevation in head-relative and world coordinates
- RT60:
    - `sabine`: frequency-band RT60 and mid-band summary (500/1000/2000 Hz)
    - `from_brir`: RT60 estimated directly from BRIR decay (T30/T20/T10 fallback)


### Contents

```
|__ DEMO.ipynb (START HERE)

|__ simulator.py (Python implementation -- revised and ported by Mark Saddler, 2023/07)

|__ simulator_matlab.py (Python interface for calling MATLAB simulator -- Mark Saddler, 2023/07)

|__ kemar_hrtfs (HRTF measurements of a KEMAR dummy-head microphone -- Gardner & Martin, 1994)

|__ materials_original.csv (absorption coefficients for different wall materials)

|__ src (MATLAB source code by Mike O'Connell and Jay Desloge)
    |__ acoeff_hrtf.m
    |__ impulse_generate_hrtf.m
    |__ shapedfilter_hrtf.m
    |__ vary_stim_env_hrir_sweep.m (script for generating set of BRIRs by Andrew Francl)

|__ generate_brir_manifest.py
|__ generate_brir_dataset.py      (code for Saddler & McDermott, 2024 Nature Communications)
|__ generate_brir_dataset_job.sh
```


### HRTF measurements of a KEMAR dummy-head microphone

The `kemar_hrtfs` included in this repository were measured by Bill Gardner and Keith Martin (Copyright 1994 by the MIT Media Laboratory). The compact wav files and documentation were downloaded from [https://sound.media.mit.edu/resources/KEMAR.html](https://sound.media.mit.edu/resources/KEMAR.html).


### Contact

Mark R. Saddler (msaddler@mit.edu / marksa@dtu.dk)


### GitHub Demo Page

This repository includes a static demo page for generated binaural audio samples:

- Demo entry: [docs/index.html](docs/index.html)
- Audio assets: [rendered_zhengxue](rendered_zhengxue)

To publish with GitHub Pages:

1. Push the repository to GitHub.
2. Go to `Settings -> Pages`.
3. Set `Build and deployment` source to `Deploy from a branch`.
4. Select branch `main` (or your release branch) and folder `/docs`.
5. Save, then open the generated Pages URL.

For local preview from the repository root:

```bash
python -m http.server 8000
```

Then open: `http://localhost:8000/docs/`
