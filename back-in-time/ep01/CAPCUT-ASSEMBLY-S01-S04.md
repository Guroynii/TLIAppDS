# CapCut Assembly — EP.01 Shot 01–04 (ทดลองตัดต่อ) · **VO v4**

> **อัปเดต:** ใช้เสียงช่วง 1 ใหม่ `ElevenLabs_2026-11-07T14_41_48_UNC3_ivc_s35_sim75_v4.mp3` (30.04 s · จบที่ "…หงุดหงิดแทบตาย")
> ตัวเลขทั้งหมดในไฟล์นี้เป็นเวลาของเสียงใหม่แล้ว

**วิดีโอเป้าหมาย:** `renders/PREVIEW_S01-S04_animatic.mp4` (เรนเดอร์จาก Keyframe เดียวกับคู่มือนี้ — ประกอบใน CapCut ให้ออกมาเหมือนไฟล์นี้)
**Asset Bundle:** `CAPCUT_EP01_S01-S04.zip` (โฟลเดอร์เรียงตามลำดับ import)

## 0. ตั้งค่าโปรเจกต์
- New Project → Ratio **16:9** · Resolution **1080p** · Frame rate **25 fps**
- Import ทั้งโฟลเดอร์ `CAPCUT_EP01_S01-S04`

## 1. Audio (แกนหลัก)
- ลาก `0_audio/VO_EP01_part1_v4.mp3` ลง Audio track เริ่มที่ **00:00:01:00** (เว้นหัว 1 วินาที) — จบที่ 31.04
- ต่อด้วย `0_audio/VO_EP01_part1-2.mp3` (ไฟล์เดิม) **Trim หัวทิ้งถึง 00:00:29:06** (29.25 s ก่อนคำว่า "วันนี้ลุงอังก์…") แล้ววางที่ **31.20** → ส่วนหลังทั้งหมดของไฟล์เดิม: Program = VO เดิม + 1.95 s
- Program TC = VO TC + 1.00 s — ตารางด้านล่างเป็น **Program TC** แล้ว (ss.ss / hh:mm:ss:ff @25fps)

## 2. Main Track

| Shot | ไฟล์ | เริ่ม | จบ | ยาว |
|---|---|---|---|---|
| 01 | `1_shot01/S01_video.mp4` (Speed **0.99×** ให้ยาวพอ) | 0.00 | 7.10 (00:00:07:03) | 7.10 |
| 02 | `2_shot02/S02_plate.png` | 7.10 | 12.60 (00:00:12:15) | 5.50 |
| 03 | `3_shot03/S03_plate.png` | 12.60 | 18.30 (00:00:18:08) | 5.70 |
| 04 | `4_shot04/S04_plate.png` | 18.30 | 22.60 (00:00:22:15) | 4.30 |
| 05 | (ลุงอังก์ — ยังไม่ทำ) | 22.60 | 31.04+ | — |

**Transitions:** 01→02 Hard cut · 02→03 Hard cut · 03→04 **Dissolve 0.5 s** · 04→(05) **Dip to white**: ใส่ Color layer สี `#FFF3E0` Opacity 0 → 100% ที่ 22.12–22.60

## 3. Overlay Tracks (ทุก Shot)
- `9_overlays/PAST_film-frame-overlay_1920x1080.png` วางยาว 0.00–22.60 บน Track บนสุด · Scale 100% · Position 0,0
- (ระหว่างทำงาน) `GUIDE_safe-area_1920x1080.png` — **ลบก่อน Export**
- Video S01 กว้าง 1912 px → Scale **100.4%**

## 4. Keyframes

### Shot 01 (0.00–7.10)
| เวลา | Layer | ค่า |
|---|---|---|
| 0.00 → 0.50 | S01_video | Opacity 0 → 100% (fade from black) |
| 0.00 → 7.10 | S01_video | Scale 100.4 → 103.4% |
| 2.98 → 3.22 | label-1 วันเสาร์ | Position **X −516, Y +319** · Scale 108 → 100% · Rotation −3° → 0° · Opacity 0 → 100% (3.10) |
| 4.02 → 4.26 | label-2 บ่าย 2 โมง | Position **X −486, Y +172** · animation เดียวกัน |

### Shot 02 (7.10–12.60)
- เข็มทั้งสอง (`hand-hour`, `hand-minute`): **Position X 0, Y +46 · Scale 66%** — ตั้งครั้งเดียว
- Plate: Scale 100 → 104% ตลอด Shot

| เวลา | เข็มสั้น (Rotation) | เข็มยาว (Rotation) |
|---|---|---|
| 7.10 – 7.25 | 60° | 0° |
| 7.25 → 7.92 (ease-out) | 60° → 67.5° | 0° → 90° |
| 10.45 → 11.10 (ease-out) | 67.5° → 75° | 90° → 180° |
| 11.10 – 12.60 | 75° | 180° |

### Shot 03 (12.60–18.30)
- ลาก `S03_L0` … `S03_L6` เรียงขึ้นตามเลข · ทุกชิ้น **Position 0,0 · Scale 100%** (ห้ามแก้)
- Plate: Scale 100 → 103%
- "เข้า" = Opacity 0 → 100% + Position Y −12 → 0 ใน 8 frames (0.32 s)

| เวลา | Layer | การเคลื่อนไหว |
|---|---|---|
| 12.60 | L0_scrim | Fade in 0.48 s |
| 12.80 | L1_panel | เข้า |
| 13.10 | L2_icon-phone | เข้า |
| 13.66 | L4_text-no-mobile | เข้า |
| 14.02 → 14.26 | L3_strike | Mask **Linear** เลื่อนเปิดจากซ้ายไปขวา |
| 16.00 | L5_bubble | เข้า |
| 17.00 → 17.24 | L5_bubble | Opacity 100 → 55% |
| 17.00 | L6_send-failed | เข้า |
| 17.85 → 18.25 | L0–L6 ทั้งหมด | Opacity → 0% |

### Shot 04 (18.30–22.60)
- Plate: Scale 106 → 100% (pull-out) ตลอด Shot
- Adjust: Temp +4, Exposure −0.05
- 22.12 → 22.60: Dip to warm white

## 5. Color (Adjustment layer 0.00–22.60)
Saturation −8 · Highlights −10 · Shadows ส้มเล็กน้อย · Grain 15–18% (Effects → Film grain)

## 6. Sound
| เวลา | SFX | ระดับ |
|---|---|---|
| 0.20 | tape play click | −16 dB |
| 2.98 / 4.02 | paper tape stick | −14 dB |
| 7.25–7.92 / 10.45–11.10 | clock tick เร่ง + tick หนักตอนหยุด | −18 dB |
| 12.80 | soft whoosh | −22 dB |
| 14.02 | marker swipe | −18 dB |
| 16.00 | message pop | −20 dB |
| 17.00 | error blip | −20 dB |
| 21.60 / 22.00 / 22.40 | clock tick เบา | −30 dB |
| 0.00–22.60 | 90s city ambience | −24 dB (Shot 04: −28 dB) |

*ใน Animatic มีแค่เสียงติ๊กนาฬิกาสังเคราะห์ชั่วคราว — SFX จริงใช้จากคลัง CapCut / royalty-free*

## 7. Export (ทดสอบ)
1080p · 25 fps · H.264 · Bitrate Recommended — เทียบกับ Animatic

---

# ส่วนต่อ: Shot 05–08 (VO ช่วง 2 v4)

## Audio
- `VO_EP01_part2_v4.mp3` วางที่ **31.40** (เว้นหลังเสียงช่วง 1 ประมาณ 0.36 s) — **ไม่ต้องใช้ไฟล์เสียงเดิม part1-2 แล้ว** สำหรับช่วงนี้
- Program = VO2 + 31.40

## Main Track
| Shot | ไฟล์ | เริ่ม | จบ |
|---|---|---|---|
| 05 | (รอคลิป lip-sync — ใช้ `S05_lipsync_…mp3` สร้างบน OpenArt) | 22.60 | 31.40 |
| 06–08 | `S06-08_host_1920x1080.mp4` (คลิปเดียวต่อเนื่อง · ปิดเสียงคลิป) | **31.40** | **44.52** |

- คลิป 06–08: Scale 100 → 103% ตลอดคลิป · Present Grade · ไม่มีกรอบฟิล์ม · Grain 8%

## Keyframes (Program TC)
| เวลา | การกระทำ |
|---|---|
| 34.70 | Split คลิป → ใส่ Blur + `S07_T0_dim` Fade in 6 frames |
| 34.82 → 35.14 | `S07_T1_title` Opacity 0 → 100% |
| 36.95 → 37.25 | Title + Dim + Blur ออก (Split คลิปที่ 37.25) |
| 38.50 | `S08_Q0_panel` เข้า (Opacity 0→100, Y −12→0, 8 frames) |
| 38.62 | `S08_Q1_line1` เข้า |
| 41.12 | `S08_Q2_line2-3` เข้า |
| 44.25 → 44.52 | Q0–Q2 Fade out |
| 34.70 | SFX tape rewind สั้น −18 dB |
