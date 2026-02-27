#!/usr/bin/env python3
"""
翻译 Features 文件中的描述文本
分批处理以避免 token 限制
"""

import json
import re
from pathlib import Path
from collections import defaultdict

# 读取已翻译名称的文件
src_path = Path("/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Features.json")
with open(src_path, 'r', encoding='utf-8') as f:
    features = json.load(f)

# 统计描述文本量
total_chars = 0
desc_count = 0
for feature in features:
    if "desc" in feature and isinstance(feature["desc"], list):
        for desc in feature["desc"]:
            if isinstance(desc, str):
                total_chars += len(desc)
                desc_count += 1

print(f"Total descriptions: {desc_count}")
print(f"Total characters: {total_chars}")

# 检查已有的翻译状态
translated_count = 0
for feature in features:
    if "desc_en" in feature:
        translated_count += 1

print(f"Features with desc_en: {translated_count}/{len(features)}")
