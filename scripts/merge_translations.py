#!/usr/bin/env python3
"""
合并所有职业翻译到最终的 Features 文件
"""

import json
from pathlib import Path

# 路径
src_path = Path("/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Features.json")
trans_dir = Path("/Users/chezi/code/java/5e-database/translations/features")
dst_path = Path("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Features.json")

# 读取源文件
with open(src_path, 'r', encoding='utf-8') as f:
    features = json.load(f)

# 创建索引到特性的映射
feature_map = {f["index"]: f for f in features}

# 加载已翻译的职业
translated_classes = ["barbarian", "bard", "fighter", "monk", "rogue", "wizard"]

for class_name in translated_classes:
    trans_file = trans_dir / f"{class_name}_translated.json"
    if trans_file.exists():
        with open(trans_file, 'r', encoding='utf-8') as f:
            trans_data = json.load(f)
        
        for item in trans_data:
            idx = item["feature_index"]
            if idx in feature_map:
                # 添加翻译的描述
                feature_map[idx]["desc_en"] = feature_map[idx]["desc"]
                feature_map[idx]["desc"] = item["desc"]

# 保存最终文件
dst_path.parent.mkdir(parents=True, exist_ok=True)
with open(dst_path, 'w', encoding='utf-8') as f:
    json.dump(features, f, ensure_ascii=False, indent=2)

print(f"Merged {len(translated_classes)} classes into {dst_path}")

# 统计
with_desc_en = sum(1 for f in features if "desc_en" in f)
print(f"Features with desc translation: {with_desc_en}/{len(features)}")
