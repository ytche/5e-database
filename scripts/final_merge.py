#!/usr/bin/env python3
"""
最终合并所有翻译
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

# 已翻译的职业（8个职业已完成完整翻译）
translated_classes = ["barbarian", "bard", "cleric", "fighter", "monk", "paladin", "rogue", "wizard"]

# 加载已翻译的职业
for class_name in translated_classes:
    trans_file = trans_dir / f"{class_name}_translated.json"
    if trans_file.exists():
        with open(trans_file, 'r', encoding='utf-8') as f:
            trans_data = json.load(f)
        
        for item in trans_data:
            idx = item["feature_index"]
            if idx in feature_map:
                # 保存原文
                original_desc = feature_map[idx]["desc"]
                # 添加翻译
                feature_map[idx]["desc_en"] = original_desc
                feature_map[idx]["desc"] = item["desc"]

# 为未翻译的职业添加标记（druid, ranger, sorcerer, warlock）
# 这些职业的desc保留英文，添加desc_en作为副本
for f in features:
    class_name = f.get("class", {}).get("name_en", f.get("class", {}).get("name", ""))
    if not any(tc in class_name.lower() for tc in translated_classes):
        if "desc_en" not in f and "desc" in f:
            f["desc_en"] = f["desc"]

# 保存最终文件
dst_path.parent.mkdir(parents=True, exist_ok=True)
with open(dst_path, 'w', encoding='utf-8') as f:
    json.dump(features, f, ensure_ascii=False, indent=2)

# 统计
with_desc_en = sum(1 for f in features if "desc_en" in f)
fully_translated = sum(1 for f in features if "desc_en" in f and f["desc"] != f["desc_en"])
print(f"总特性数: {len(features)}")
print(f"已添加desc_en: {with_desc_en}/{len(features)}")
print(f"完整翻译（中文+英文）: {fully_translated}/{len(features)}")
print(f"仅保留英文: {with_desc_en - fully_translated}/{len(features)}")
print(f"输出文件: {dst_path}")
