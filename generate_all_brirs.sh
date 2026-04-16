#!/bin/bash
# generate_all_brirs.sh
# 按场景参数(房间尺寸、材质、头位、声源距离)批量仿真 BRIR。
# 每个场景生成两个方位：前方(az000_el+00)和左方(az090_el+00)。
#
# 使用方法:
#   bash generate_all_brirs.sh
#
# 可选环境变量:
#   OUT_DIR=output/scenes
#   MATERIALS_CSV=materials_original.csv
#   SR=44100
#   PROCESSES=8
#
# 说明:
# - 这里沿用“旧版 .sh 参数控制”的方式调用 simulate_brir_with_meta.py。
# - room-materials 顺序为: [x0, x1, y0, y1, floor, ceiling]

set -euo pipefail

SCRIPT="python simulate_brir_with_meta.py"
OUT_DIR="${OUT_DIR:-output/scenes}"
MATERIALS_CSV="${MATERIALS_CSV:-materials_original.csv}"
SR="${SR:-44100}"
PROCESSES="${PROCESSES:-8}"

if [[ ! -f "$MATERIALS_CSV" ]]; then
  echo "ERROR: materials csv not found: $MATERIALS_CSV" >&2
  exit 1
fi

validate_material_ids() {
  local room_materials="$1"
  local scene_id="$2"
  local id

  for id in ${room_materials//,/ }; do
    if ! awk -F, -v target_id="$id" 'NR > 1 && $1 == target_id {found = 1} END {exit(found ? 0 : 1)}' "$MATERIALS_CSV"; then
      echo "ERROR: scene '$scene_id' uses material id '$id' not found in $MATERIALS_CSV" >&2
      exit 1
    fi
  done
}

run_one_direction() {
  local scene_id="$1"
  local scene_cn="$2"
  local room_materials="$3"
  local room_dim="$4"
  local head_pos="$5"
  local src_azim="$6"
  local src_dist="$7"
  local dur="$8"
  local suffix="$9"

  local out_prefix="${OUT_DIR}/${scene_id}/${scene_id}_${suffix}"

  echo ""
  echo ">>> ${scene_cn} (${suffix})"
  echo "    room_materials=${room_materials}"
  echo "    room_dim_xyz=${room_dim}"
  echo "    head_pos_xyz=${head_pos}"
  echo "    src_azim=${src_azim}, src_dist=${src_dist}, dur=${dur}"

  $SCRIPT \
    --room-materials "$room_materials" \
    --room-dim-xyz "$room_dim" \
    --head-pos-xyz "$head_pos" \
    --head-azim 0 \
    --src-azim "$src_azim" --src-elev 0 --src-dist "$src_dist" \
    --sr "$SR" --dur "$dur" --processes "$PROCESSES" \
    --out-prefix "$out_prefix" \
    --strict
}

echo "============================================"
echo " Generating BRIRs for configured scenes"
echo "============================================"
echo "materials csv : $MATERIALS_CSV"
echo "output dir    : $OUT_DIR"
echo "sr            : $SR"
echo "processes     : $PROCESSES"
echo ""

mkdir -p "$OUT_DIR"

# scene_id|scene_cn|room_materials|room_dim_xyz|head_pos_xyz|src_dist_front|src_dist_left|dur
# 本表根据 materials.csv 的材质 ID 进行参数化设置。
SCENE_PRESETS=(
  "01-anechoic_chamber|消声室|26,26,26,26,26,26|8,6,3|4,3,1.5|2.0|2.0|0.35"
  "02-recording_studio|录音棚|9,9,9,9,15,20|6,5,3|3,2.5,1.5|1.4|1.2|0.8"
  "03-car_interior|车内|6,6,6,6,14,16|2.6,1.8,1.4|1.3,0.9,1.0|0.8|0.6|0.4"
  "04-small_bedroom|小卧室|5,5,5,5,14,16|4.5,3.5,2.8|2.25,1.75,1.4|1.3|1.1|0.9"
  "05-office|办公室|5,5,5,5,13,17|8,6,3|4,3,1.5|1.6|1.4|1.0"
  "06-living_room|客厅|5,5,5,5,12,16|7,5,3|3.5,2.5,1.4|2.0|1.6|1.2"
  "07-small_meeting_room|小会议室|8,8,8,8,14,17|6.5,4.8,3|3.25,2.4,1.5|1.8|1.4|1.1"
  "08-classroom|教室|7,7,7,7,13,19|10,7,3.5|5,3.5,1.5|2.4|1.8|1.4"
  "09-small_concert_hall|小音乐厅|11,11,11,11,15,19|20,14,9|10,7,1.5|6.0|4.5|2.5"
  "10-open_office|开放办公区|7,7,7,7,14,17|18,12,3.2|9,6,1.5|2.5|2.0|1.4"
  "11-bathroom_tile|瓷砖浴室|4,4,4,4,13,16|3.2,2.4,2.8|1.6,1.2,1.5|1.2|0.9|1.2"
  "12-medium_theater|中型剧院|2,2,2,2,15,19|24,18,10|12,9,1.5|7.0|5.0|2.8"
  "13-indoor_gymnasium|室内体育馆|2,2,2,2,12,16|30,18,9|15,9,1.6|8.0|6.0|3.0"
  "14-large_concert_hall|大音乐厅|2,2,2,2,15,19|45,30,16|22.5,15,1.6|12.0|8.0|3.6"
  "15-corridor_stairwell|走廊楼梯间|2,2,2,2,13,16|20,4,4|10,2,1.5|4.0|1.4|2.0"
  "16-tunnel_parking|地下通道停车场|2,2,2,2,13,16|50,10,4|25,5,1.6|6.0|3.0|2.4"
  "17-cathedral|大教堂|4,4,4,4,4,4|70,35,28|35,17.5,1.7|18.0|10.0|4.5"
  "18-large_stone_church|大型石质教堂|4,4,4,4,4,4|50,24,20|25,12,1.7|14.0|8.0|4.0"
  "19-outdoor_open|室外开阔|24,24,24,24,23,26|80,80,20|40,40,1.7|12.0|10.0|1.0"
  "20-urban_street|城市街道|2,2,2,2,24,26|120,30,20|60,15,1.7|15.0|8.0|1.5"
  "21-forest|森林|23,23,23,23,23,26|60,60,25|30,30,1.7|10.0|8.0|1.2"
)

TOTAL_SCENES=${#SCENE_PRESETS[@]}
TOTAL_TASKS=$((TOTAL_SCENES * 2))

echo "Configured scenes : $TOTAL_SCENES"
echo "Total BRIR tasks  : $TOTAL_TASKS (front + left)"

task_idx=0
for preset in "${SCENE_PRESETS[@]}"; do
  IFS='|' read -r scene_id scene_cn room_materials room_dim head_pos src_dist_front src_dist_left dur <<< "$preset"

  validate_material_ids "$room_materials" "$scene_id"

  task_idx=$((task_idx + 1))
  echo ""
  echo "[$task_idx/$TOTAL_TASKS] ${scene_id} az000_el+00"
  run_one_direction "$scene_id" "$scene_cn-前方" "$room_materials" "$room_dim" "$head_pos" 0 "$src_dist_front" "$dur" "front"

  task_idx=$((task_idx + 1))
  echo ""
  echo "[$task_idx/$TOTAL_TASKS] ${scene_id} az090_el+00"
  run_one_direction "$scene_id" "$scene_cn-左方" "$room_materials" "$room_dim" "$head_pos" 90 "$src_dist_left" "$dur" "left"
done

echo ""
echo "============================================"
echo " All done"
echo "============================================"
echo "Output files in: ${OUT_DIR}/"
echo ""
find "$OUT_DIR" -type f \( -name "*.wav" -o -name "*.meta.json" \) | sort