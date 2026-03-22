import os
import math
import json
from PIL import Image
from pixelmatch.pypixelmatch import pixelmatch

def assert_snapshot(page, snapshot_name, threshold=0.1, mismatch_tolerance=0.01):
    """
    Take a screenshot of the current page and compare it with the baseline.
    If the baseline does not exist, it will be created.
    """
    work_dir = os.getcwd()
    baseline_dir = os.path.join(work_dir, 'snapshots', 'baseline')
    diff_dir = os.path.join(work_dir, 'snapshots', 'diff')
    actual_dir = os.path.join(work_dir, 'snapshots', 'actual')
    
    os.makedirs(baseline_dir, exist_ok=True)
    os.makedirs(diff_dir, exist_ok=True)
    os.makedirs(actual_dir, exist_ok=True)
    
    baseline_path = os.path.join(baseline_dir, f"{snapshot_name}.png")
    actual_path = os.path.join(actual_dir, f"{snapshot_name}.png")
    diff_path = os.path.join(diff_dir, f"{snapshot_name}.png")
    
    page.screenshot(path=actual_path, full_page=True)
    
    vision_results_path = os.path.join(work_dir, 'vision_results.json')
    results = []
    if os.path.exists(vision_results_path):
        try:
            with open(vision_results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
        except Exception:
            pass
            
    if not os.path.exists(baseline_path):
        print(f"[{snapshot_name}] Baseline not found. Saving current screenshot as baseline.")
        page.screenshot(path=baseline_path, full_page=True)
        results.append({
            "name": snapshot_name,
            "status": "new",
            "mismatch_ratio": 0
        })
        with open(vision_results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f)
        return True
        
    img_baseline = Image.open(baseline_path)
    img_actual = Image.open(actual_path)
    
    if img_baseline.size != img_actual.size:
        print(f"[{snapshot_name}] Snapshot size mismatch: baseline {img_baseline.size} vs actual {img_actual.size}")
        img_actual = img_actual.resize(img_baseline.size)
        
    img_diff = Image.new("RGBA", img_baseline.size)
    
    mismatch = pixelmatch(
        img_baseline,
        img_actual,
        img_diff,
        threshold=threshold,
        includeAA=True
    )
    
    total_pixels = img_baseline.size[0] * img_baseline.size[1]
    mismatch_ratio = mismatch / total_pixels
    
    is_pass = mismatch_ratio <= mismatch_tolerance
    
    if not is_pass:
        img_diff.save(diff_path)
        
    results.append({
        "name": snapshot_name,
        "status": "passed" if is_pass else "failed",
        "mismatch_ratio": mismatch_ratio,
        "mismatch_pixels": mismatch,
        "total_pixels": total_pixels
    })
    
    with open(vision_results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f)
        
    if not is_pass:
        raise AssertionError(f"Snapshot mismatch for '{snapshot_name}': {mismatch} pixels differ ({mismatch_ratio*100:.2f}%). Diff saved to {diff_path}")
        
    return True

