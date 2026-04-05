#!/usr/bin/env python
"""
Simple script to save motion analysis visualization frames with density heatmap overlay.
Method 1: Save frames without display windows.
"""

import scipy.io
import numpy as np
from pathlib import Path

from src.motion_analysis import process

print("Motion Analysis with Density Heatmap - Frame Saving")
print("=" * 60)

# Get user input
try:
    end_frame = int(input("How many frames to process? (default 50): ") or "50")
except ValueError:
    end_frame = 50

print(f"\nProcessing first {end_frame} frames...")
print("(This generates motion analysis visualizations as PNG images)")
print("-" * 60)

# Load mall dataset density data
print("Loading mall dataset density data...")
mall_gt_path = Path('mall_dataset/mall_gt.mat')
density_data = {}
if mall_gt_path.exists():
    try:
        mall_gt = scipy.io.loadmat(str(mall_gt_path))
        if 'frame' in mall_gt:
            frame_data = mall_gt['frame']
            if frame_data.dtype == object and frame_data.size > 0:
                actual_frames = frame_data[0]  # Array of structs
                print(f"actual_frames shape: {actual_frames.shape}, dtype: {actual_frames.dtype}")
                for i in range(min(len(actual_frames), end_frame)):
                    frame_struct = actual_frames[i]
                    if hasattr(frame_struct, 'dtype') and frame_struct.dtype.names and 'loc' in frame_struct.dtype.names:
                        loc = frame_struct['loc']
                        if loc.size > 0 and loc.ndim == 2:
                            points = loc.astype(float)
                            density_data[i] = [(float(x), float(y)) for x, y in points]
                print(f"Loaded density data for {len(density_data)} frames")
            else:
                print("Frame data not in expected object format")
        else:
            print("No 'frame' key in mall_gt.mat")
    except Exception as e:
        print(f"Error loading density data: {e}")
else:
    print("mall_gt.mat not found, proceeding without density overlay")

# Process and save frames
stats = process(
    'mall_dataset/frames',
    end_idx=end_frame,
    display=False,           # No windows
    save_frames=True,        # Save as PNG images
    start_idx=0,
    skip_frames=1,
    density_data=density_data if density_data else None
)

# Show results
print("\n" + "=" * 60)
print("SAVED FRAMES LOCATION: output_frames/")
print("Each frame contains 4 panels: density heatmap | flow arrows")
print("                           zone overlay    | motion heatmap")
print("=" * 60)

# Count saved files
output_dir = Path('output_frames')
saved_files = list(output_dir.glob('frame_*.png'))
if saved_files:
    print(f"✓ {len(saved_files)} visualization frames saved")
    print(f"✓ First frame: {output_dir / saved_files[0].name}")
    print(f"✓ Last frame: {output_dir / saved_files[-1].name}")
    print("\nYou can now:")
    print("  1. Open output_frames/ folder in Windows Explorer")
    print("  2. View PNG images (double-click to open)")
    print("  3. Use Windows Photo Viewer to browse through them")
else:
    print("✗ No frames were saved")

print("\nStatistics:")
print(f"  Total pairs: {stats['total_pairs']}")
print(f"  Processed: {stats['processed']}")
print(f"  Mean speed: {stats.get('mean_avg_speed', 0):.2f} px/frame")
print(f"  Max speed: {stats.get('mean_max_speed', 0):.2f} px/frame")

if __name__ == "__main__":
    source_path = r"C:\Users\Lokesh Kumar\Downloads\mall_dataset\mall_dataset\frames"
    process(source_path, display=True)