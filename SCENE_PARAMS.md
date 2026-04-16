# BRIR 21场景参数清单

本文件对应脚本 generate_all_brirs.sh 中的 SCENE_PRESETS 参数。

参数约定：
- room_materials 顺序: [x0, x1, y0, y1, floor, ceiling]
- room_dim_xyz: X,Y,Z (m)
- head_pos_xyz: X,Y,Z (m)
- 前方方位: az000_el+00, src_azim=0
- 左方方位: az090_el+00, src_azim=90

---

## 场景01: 01-anechoic_chamber (消声室)
- room_materials: 26,26,26,26,26,26
- room_dim_xyz: 8,6,3
- head_pos_xyz: 4,3,1.5
- src_dist_front: 2.0
- src_dist_left: 2.0
- dur: 0.35

## 场景02: 02-recording_studio (录音棚)
- room_materials: 9,9,9,9,15,20
- room_dim_xyz: 6,5,3
- head_pos_xyz: 3,2.5,1.5
- src_dist_front: 1.4
- src_dist_left: 1.2
- dur: 0.8

## 场景03: 03-car_interior (车内)
- room_materials: 6,6,6,6,14,16
- room_dim_xyz: 2.6,1.8,1.4
- head_pos_xyz: 1.3,0.9,1.0
- src_dist_front: 0.8
- src_dist_left: 0.6
- dur: 0.4

## 场景04: 04-small_bedroom (小卧室)
- room_materials: 5,5,5,5,14,16
- room_dim_xyz: 4.5,3.5,2.8
- head_pos_xyz: 2.25,1.75,1.4
- src_dist_front: 1.3
- src_dist_left: 1.1
- dur: 0.9

## 场景05: 05-office (办公室)
- room_materials: 5,5,5,5,13,17
- room_dim_xyz: 8,6,3
- head_pos_xyz: 4,3,1.5
- src_dist_front: 1.6
- src_dist_left: 1.4
- dur: 1.0

## 场景06: 06-living_room (客厅)
- room_materials: 5,5,5,5,12,16
- room_dim_xyz: 7,5,3
- head_pos_xyz: 3.5,2.5,1.4
- src_dist_front: 2.0
- src_dist_left: 1.6
- dur: 1.2

## 场景07: 07-small_meeting_room (小会议室)
- room_materials: 8,8,8,8,14,17
- room_dim_xyz: 6.5,4.8,3
- head_pos_xyz: 3.25,2.4,1.5
- src_dist_front: 1.8
- src_dist_left: 1.4
- dur: 1.1

## 场景08: 08-classroom (教室)
- room_materials: 7,7,7,7,13,19
- room_dim_xyz: 10,7,3.5
- head_pos_xyz: 5,3.5,1.5
- src_dist_front: 2.4
- src_dist_left: 1.8
- dur: 1.4

## 场景09: 09-small_concert_hall (小音乐厅)
- room_materials: 11,11,11,11,15,19
- room_dim_xyz: 20,14,9
- head_pos_xyz: 10,7,1.5
- src_dist_front: 6.0
- src_dist_left: 4.5
- dur: 2.5

## 场景10: 10-open_office (开放办公区)
- room_materials: 7,7,7,7,14,17
- room_dim_xyz: 18,12,3.2
- head_pos_xyz: 9,6,1.5
- src_dist_front: 2.5
- src_dist_left: 2.0
- dur: 1.4

## 场景11: 11-bathroom_tile (瓷砖浴室)
- room_materials: 4,4,4,4,13,16
- room_dim_xyz: 3.2,2.4,2.8
- head_pos_xyz: 1.6,1.2,1.5
- src_dist_front: 1.2
- src_dist_left: 0.9
- dur: 1.2

## 场景12: 12-medium_theater (中型剧院)
- room_materials: 2,2,2,2,15,19
- room_dim_xyz: 24,18,10
- head_pos_xyz: 12,9,1.5
- src_dist_front: 7.0
- src_dist_left: 5.0
- dur: 2.8

## 场景13: 13-indoor_gymnasium (室内体育馆)
- room_materials: 2,2,2,2,12,16
- room_dim_xyz: 30,18,9
- head_pos_xyz: 15,9,1.6
- src_dist_front: 8.0
- src_dist_left: 6.0
- dur: 3.0

## 场景14: 14-large_concert_hall (大音乐厅)
- room_materials: 2,2,2,2,15,19
- room_dim_xyz: 45,30,16
- head_pos_xyz: 22.5,15,1.6
- src_dist_front: 12.0
- src_dist_left: 8.0
- dur: 3.6

## 场景15: 15-corridor_stairwell (走廊楼梯间)
- room_materials: 2,2,2,2,13,16
- room_dim_xyz: 20,4,4
- head_pos_xyz: 10,2,1.5
- src_dist_front: 4.0
- src_dist_left: 1.4
- dur: 2.0

## 场景16: 16-tunnel_parking (地下通道停车场)
- room_materials: 2,2,2,2,13,16
- room_dim_xyz: 50,10,4
- head_pos_xyz: 25,5,1.6
- src_dist_front: 6.0
- src_dist_left: 3.0
- dur: 2.4

## 场景17: 17-cathedral (大教堂)
- room_materials: 4,4,4,4,4,4
- room_dim_xyz: 70,35,28
- head_pos_xyz: 35,17.5,1.7
- src_dist_front: 18.0
- src_dist_left: 10.0
- dur: 4.5

## 场景18: 18-large_stone_church (大型石质教堂)
- room_materials: 4,4,4,4,4,4
- room_dim_xyz: 50,24,20
- head_pos_xyz: 25,12,1.7
- src_dist_front: 14.0
- src_dist_left: 8.0
- dur: 4.0

## 场景19: 19-outdoor_open (室外开阔)
- room_materials: 24,24,24,24,23,26
- room_dim_xyz: 80,80,20
- head_pos_xyz: 40,40,1.7
- src_dist_front: 12.0
- src_dist_left: 10.0
- dur: 1.0

## 场景20: 20-urban_street (城市街道)
- room_materials: 2,2,2,2,24,26
- room_dim_xyz: 120,30,20
- head_pos_xyz: 60,15,1.7
- src_dist_front: 15.0
- src_dist_left: 8.0
- dur: 1.5

## 场景21: 21-forest (森林)
- room_materials: 23,23,23,23,23,26
- room_dim_xyz: 60,60,25
- head_pos_xyz: 30,30,1.7
- src_dist_front: 10.0
- src_dist_left: 8.0
- dur: 1.2

---

说明：
- 以上参数与 generate_all_brirs.sh 当前 SCENE_PRESETS 保持一致。
- 如需微调 RT60 倾向，优先调整 room_materials 与 room_dim_xyz，其次调整 dur。
