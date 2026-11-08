# CapCut Assembly — EP.01 Shot 01–04 (ทดลองตัดต่อ)

**วิดีโอเป้าหมาย:** `renders/PREVIEW_S01-S04_animatic.mp4` (เรนเดอร์จาก Keyframe เดียวกับคู่มือนี้ — ประกอบใน CapCut ให้ออกมาเหมือนไฟล์นี้)
**Asset Bundle:** `CAPCUT_EP01_S01-S04.zip` (โฟลเดอร์เรียงตามลำดับ import)

## 0. ตั้งค่าโปรเจกต์
- New Project → Ratio **16:9** · Resolution **1080p** · Frame rate **25 fps**
- Import ทั้งโฟลเดอร์ `CAPCUT_EP01_S01-S04`

## 1. Audio (แกนหลัก)
- ลาก `0_audio/VO_EP01_part1-2.mp3` ลง Audio track เริ่มที่ **00:00:01:00** (เว้นหัว 1 วินาที)
- Program TC = VO TC + 1.00 s — ตารางด้านล่างเป็น **Program TC** แล้ว (ss.ss / hh:mm:ss:ff @25fps)

## 2. Main Track

| Shot | ไฟล์ | เริ่ม | จบ | ยาว |
|---|---|---|---|---|
| 01 | `1_shot01/S01_video.mp4` (Speed 0.92× ให้ยาวพอ หรือตัดที่ 6.40) | 0.00 | 6.40 (00:00:06:10) | 6.40 |
| 02 | `2_shot02/S02_plate.png` | 6.40 | 10.95 (00:00:10:24) | 4.55 |
| 03 | `3_shot03/S03_plate.png` | 10.95 | 17.20 (00:00:17:05) | 6.25 |
| 04 | `4_shot04/S04_plate.png` | 17.20 | 20.70 (00:00:20:18) | 3.50 |

**Transitions:** 01→02 Hard cut · 02→03 Hard cut · 03→04 **Dissolve 0.5 s** · 04→(05) **Dip to white**: ใส่ Color layer สี `#FFF3E0` Opacity 0 → 100% ที่ 20.22–20.70

## 3. Overlay Tracks (ทุก Shot)
- `9_overlays/PAST_film-frame-overlay_1920x1080.png` วางยาว 0.00–20.70 บน Track บนสุด · Scale 100% · Position 0,0
- (ระหว่างทำงาน) `GUIDE_safe-area_1920x1080.png` — **ลบก่อน Export**
- Video S01 กว้าง 1912 px → Scale **100.4%**

## 4. Keyframes

### Shot 01 (0.00–6.40)
| เวลา | Layer | ค่า |
|---|---|---|
| 0.00 → 0.50 | S01_video | Opacity 0 → 100% (fade from black) |
| 0.00 → 6.40 | S01_video | Scale 100.4 → 103.4% |
| 2.94 → 3.18 | label-1 วันเสาร์ | Position **X −516, Y +319** · Scale 108 → 100% · Rotation −3° → 0° · Opacity 0 → 100% (3.06) |
| 3.44 → 3.68 | label-2 บ่าย 2 โมง | Position **X −486, Y +172** · animation เดียวกัน |

### Shot 02 (6.40–10.95)
- เข็มทั้งสอง (`hand-hour`, `hand-minute`): **Position X 0, Y +46 · Scale 66%** — ตั้งครั้งเดียว
- Plate: Scale 100 → 104% ตลอด Shot

| เวลา | เข็มสั้น (Rotation) | เข็มยาว (Rotation) |
|---|---|---|
| 6.40 – 6.55 | 60° | 0° |
| 6.55 → 7.10 (ease-out) | 60° → 67.5° | 0° → 90° |
| 9.20 → 9.82 (ease-out) | 67.5° → 75° | 90° → 180° |
| 9.82 – 10.95 | 75° | 180° |

### Shot 03 (10.95–17.20)
- ลาก `S03_L0` … `S03_L6` เรียงขึ้นตามเลข · ทุกชิ้น **Position 0,0 · Scale 100%** (ห้ามแก้)
- Plate: Scale 100 → 103%
- "เข้า" = Opacity 0 → 100% + Position Y −12 → 0 ใน 8 frames (0.32 s)

| เวลา | Layer | การเคลื่อนไหว |
|---|---|---|
| 10.95 | L0_scrim | Fade in 0.48 s |
| 11.00 | L1_panel | เข้า |
| 11.30 | L2_icon-phone | เข้า |
| 12.20 | L4_text-no-mobile | เข้า |
| 12.46 → 12.70 | L3_strike | Mask **Linear** เลื่อนเปิดจากซ้ายไปขวา |
| 14.70 | L5_bubble | เข้า |
| 15.80 → 16.04 | L5_bubble | Opacity 100 → 55% |
| 15.80 | L6_send-failed | เข้า |
| 16.80 → 17.20 | L0–L6 ทั้งหมด | Opacity → 0% |

### Shot 04 (17.20–20.70)
- Plate: Scale 106 → 100% (pull-out) ตลอด Shot
- Adjust: Temp +4, Exposure −0.05
- 20.22 → 20.70: Dip to warm white

## 5. Color (Adjustment layer 0.00–20.70)
Saturation −8 · Highlights −10 · Shadows ส้มเล็กน้อย · Grain 15–18% (Effects → Film grain)

## 6. Sound
| เวลา | SFX | ระดับ |
|---|---|---|
| 0.20 | tape play click | −16 dB |
| 2.94 / 3.44 | paper tape stick | −14 dB |
| 6.55–7.10 / 9.20–9.82 | clock tick เร่ง + tick หนักตอนหยุด | −18 dB |
| 11.00 | soft whoosh | −22 dB |
| 12.46 | marker swipe | −18 dB |
| 14.70 | message pop | −20 dB |
| 15.80 | error blip | −20 dB |
| 19.70 / 20.10 / 20.50 | clock tick เบา | −30 dB |
| 0.00–20.70 | 90s city ambience | −24 dB (Shot 04: −28 dB) |

*ใน Animatic มีแค่เสียงติ๊กนาฬิกาสังเคราะห์ชั่วคราว — SFX จริงใช้จากคลัง CapCut / royalty-free*

## 7. Export (ทดสอบ)
1080p · 25 fps · H.264 · Bitrate Recommended — เทียบกับ Animatic
