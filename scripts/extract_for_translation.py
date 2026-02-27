#!/usr/bin/env python3
"""
提取需要翻译的描述文本，按职业分组
"""

import json
from pathlib import Path
from collections import defaultdict

src_path = Path("/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Features.json")
dst_dir = Path("/Users/chezi/code/java/5e-database/translations/features")
dst_dir.mkdir(parents=True, exist_ok=True)

with open(src_path, 'r', encoding='utf-8') as f:
    features = json.load(f)

# 按职业分组
by_class = defaultdict(list)
for i, feature in enumerate(features):
    class_name = feature.get("class", {}).get("name", "Unknown")
    by_class[class_name].append((i, feature))

# 为每个职业创建翻译文件
for class_name in sorted(by_class.keys()):
    items = by_class[class_name]
    output = []
    
    for idx, feature in items:
        feature_index = feature.get("index", f"idx_{idx}")
        feature_name = feature.get("name", "")
        desc_list = feature.get("desc", [])
        
        entry = {
            "feature_index": feature_index,
            "feature_name": feature_name,
            "desc": desc_list if isinstance(desc_list, list) else [desc_list],
        }
        output.append(entry)
    
    # 保存为JSON
    output_path = dst_dir / f"{class_name.lower()}_to_translate.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # 统计
    total_chars = sum(sum(len(d) for d in e["desc"] if d) for e in output)
    print(f"{class_name}: {len(output)} features, {total_chars} chars -> {output_path.name}")

print(f"\nAll files saved to: {dst_dir}")
