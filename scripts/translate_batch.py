#!/usr/bin/env python3
"""
按职业分批翻译 Features 描述
"""

import json
from pathlib import Path
from collections import defaultdict

src_path = Path("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Features.json")
with open(src_path, 'r', encoding='utf-8') as f:
    features = json.load(f)

# 按职业分组
by_class = defaultdict(list)
for i, feature in enumerate(features):
    class_name = feature.get("class", {}).get("name_en", feature.get("class", {}).get("name", "Unknown"))
    by_class[class_name].append((i, feature))

# 统计每个职业的描述字符数
print("Description statistics by class:\n")
for class_name in sorted(by_class.keys()):
    items = by_class[class_name]
    total_chars = 0
    for idx, feature in items:
        if "desc" in feature and isinstance(feature["desc"], list):
            for desc in feature["desc"]:
                if isinstance(desc, str):
                    total_chars += len(desc)
    print(f"{class_name}: {len(items)} features, {total_chars} chars")

print(f"\nTotal: {len(features)} features")
