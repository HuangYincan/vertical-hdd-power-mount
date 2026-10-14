"""Render the saved Blender assembly animation and encode an MP4 with FFmpeg.

Usage:
    blender --background --python scripts/render_animation.py -- --samples 32
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import bpy


def main():
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=repo / 'renders/assembly.mp4')
    parser.add_argument('--samples', type=int, default=32)
    parser.add_argument('--resolution-scale', type=int, default=100)
    extra = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    args = parser.parse_args(extra)
    if args.samples < 1:
        parser.error('--samples must be positive')
    if not 1 <= args.resolution_scale <= 100:
        parser.error('--resolution-scale must be between 1 and 100')
    ffmpeg = shutil.which('ffmpeg')
    if not ffmpeg:
        raise RuntimeError('FFmpeg is required; install it before rendering.')

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    # Keep each export's frames in its own directory.
    frames = output.parent / (output.stem + '_frames')
    frames.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(repo / 'assets/blender/hdd_power_assembly_animation.blend'))
    scene = bpy.data.scenes['HDD_Power_Assembly']
    bpy.context.window.scene = scene
    scene.render.resolution_percentage = args.resolution_scale
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'
    scene.render.filepath = str(frames / 'frame_')
    scene.render.use_file_extension = True
    if hasattr(scene, 'eevee') and hasattr(scene.eevee, 'taa_render_samples'):
        scene.eevee.taa_render_samples = args.samples
    scene.frame_set(scene.frame_start)
    bpy.ops.render.render(animation=True, scene=scene.name)
    subprocess.run([
        ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
        '-framerate', f'{scene.render.fps}/{scene.render.fps_base:g}',
        '-start_number', str(scene.frame_start),
        '-i', str(frames / 'frame_%04d.png'),
        '-frames:v', str(scene.frame_end - scene.frame_start + 1),
        # Ensure even output dimensions for H.264 / yuv420p.
        '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',
        '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
        '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an', str(output),
    ], check=True)
    print(f'Video saved: {output}')


if __name__ == '__main__':
    main()
