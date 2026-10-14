# Blender 模型与装配动画

本目录说明竖置硬盘、电源及打印挂架的装配场景。Blender 文件制作于 Blender 5.2.2 LTS；重新渲染建议使用同版本或兼容版本。

## 文件

| 路径 | 内容 |
| --- | --- |
| [`../assets/blender/hdd_power_assembly.blend`](../assets/blender/hdd_power_assembly.blend) | 静态装配，含三个模型、六颗固定螺丝、灯光和相机 |
| [`../assets/blender/hdd_power_assembly_animation.blend`](../assets/blender/hdd_power_assembly_animation.blend) | 可编辑装配动画，1–240 帧，30 fps |
| [`../assets/video/hdd_power_assembly_animation.mp4`](../assets/video/hdd_power_assembly_animation.mp4) | 已渲染的 8 秒 1080p 视频，H.264，无音轨 |
| [`../assets/images/hdd_power_animation_poster.png`](../assets/images/hdd_power_animation_poster.png) | 动画最后一帧 |
| [`../assets/images/hdd_power_assembly_preview.png`](../assets/images/hdd_power_assembly_preview.png) | 静态装配预览 |
| [`../cad/手工2.FCStd`](../cad/手工2.FCStd) | 用户提供的 FreeCAD 设计参考源文件 |
| [`../硬盘电源挂架_竖置.stl`](../硬盘电源挂架_竖置.stl) | 实际打印的挂架网格，Blender 挂架的几何来源 |
| [`../scripts/render_animation.py`](../scripts/render_animation.py) | 从保存的动画文件重新渲染 PNG 帧并编码 MP4 |

仓库原有的 `硬盘电源挂架_竖置.stl` 与用户确认的最终打印文件 `电源硬盘挂架（竖置）.stl` 字节一致，因此沿用原有名称。其 SHA-256 为：

```text
b49a483684258915dd56524634a02c9f3d44a52ce9fa03bdd5b06618580a739b
```

FreeCAD 文件作为设计参考保留；实际挂架外形以该 STL 为准。

## 装配关系

面向带三插电源口的前面板时，左右顺序为：

```text
硬盘  ← 4 颗固定螺丝 →  挂架  ← 2 颗固定螺丝 →  电源
```

- 鑫谷数智 DM-850G 竖置：宽 86 mm、深 125 mm、高 150 mm。
- 硬盘位于挂架左侧，挂架位于电源左侧；硬盘标签面朝外。
- 挂架的两个前侧安装耳与电源前面板贴合，两颗螺丝穿过 STL 上相应的孔。
- 四颗硬盘螺丝沿挂架侧板长孔连接硬盘；侧板与电源之间保留螺丝头的展示空间。
- Blender 场景使用米作为内部坐标单位，界面显示毫米；STL 以毫米导入并缩放为 0.001。

## 模型精度

| 模型 | 外形尺寸 | 几何依据 |
| --- | --- | --- |
| 挂架 | 29 × 120 × 143 mm | 最终打印 STL，保留原有孔和长孔 |
| WD Blue 4TB 3.5 英寸硬盘 | 147 × 101.6 × 26.1 mm | 常见 3.5 英寸外形，标签、连接器和外壳细节为展示用简化 |
| 鑫谷数智 DM-850G | 125 × 150 × 86 mm；竖置后高 150 mm | 产品参考图和外形尺寸；风扇、通风口、插口与外壳细节为展示用简化 |

两款硬件模型与螺丝用于说明装配、制作视频；精确接口、内部结构、螺纹及加工尺寸仍应以实物和厂商机械图纸为准。

## 对象层级

打开 `.blend` 后选择 `HDD_Power_Assembly` 场景。模型和螺丝在 `HDD_POWER_ASSEMBLY` 集合中：

| 集合 | 根节点 | 用途 |
| --- | --- | --- |
| `01_MOUNT_BRACKET` | `MOUNT_BRACKET_ROOT` | 移动整个挂架 |
| `02_WD_BLUE_4TB_HDD` | `WD_BLUE_4TB_ROOT` | 移动硬盘及外观细节 |
| `03_XINGU_DM850G_PSU` | `XINGU_DM850G_ROOT` | 移动电源及外观细节 |
| `04_ASSEMBLY_FASTENERS` | `HDD_Mount_Screw_01`–`04`、`PSU_Mount_Screw_01`–`02` | 六颗螺丝可分别移动、旋转 |
| `90_PRESENTATION` | 相机、灯光、地面与相机目标 | 演示环境 |

调整装配位置时选择对应根节点。动画文件保留部件位移、螺丝旋转及镜头运动关键帧，可继续修改为爆炸动画。

## 动画时间线

| 帧数 | 时间（约） | 内容 |
| --- | --- | --- |
| 1–18 | 0–0.6 秒 | 展示分开的硬盘、挂架、电源和六颗螺丝 |
| 19–52 | 0.6–1.7 秒 | 硬盘与挂架贴合 |
| 56–92 | 1.8–3.1 秒 | 四颗硬盘螺丝依次旋转锁紧 |
| 104–153 | 3.4–5.1 秒 | 硬盘与挂架整组合拢到电源 |
| 158–192 | 5.2–6.4 秒 | 两颗电源固定螺丝旋转锁紧 |
| 193–240 | 6.4–8 秒 | 轻微转镜展示完整装配 |

四颗硬盘螺丝先锁紧，便于在镜头中观察侧板连接。时间线已添加对应阶段标记。

## 重新渲染

先安装 Blender 和 FFmpeg，再在仓库根目录执行：

```bash
blender --background --python scripts/render_animation.py -- --samples 32
```

默认生成 `renders/assembly.mp4` 和 `renders/assembly_frames/frame_0001.png` 至 `frame_0240.png`。`renders/` 已加入忽略规则。

快速检查可降低渲染比例；导出尺寸若为奇数，编码时会补齐到偶数，以兼容 H.264：

```bash
blender --background --python scripts/render_animation.py -- --resolution-scale 50 --samples 16
```

自定义输出位置：

```bash
blender --background --python scripts/render_animation.py -- --output renders/custom.mp4
```

脚本依据自己的路径定位仓库，使用参数列表调用 FFmpeg；无需修改本机用户名或绝对路径。已提交的 MP4 为 1920 × 1080、30 fps、240 帧、8 秒，采用 `yuv420p` 并开启快速播放头信息。
