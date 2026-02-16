# 5e-SRD-Magic-Items 翻译审查报告

## 审查统计
- 审查时间：2026-02-16 22:40:20
- 审查物品总数：362
- 问题数量：5

## 总体评估

### 术语一致性 ✓
- 装备分类翻译正确：奇物、药水、戒指、武器、护甲、魔杖、法杖、卷轴、权杖、弹药
- 稀有度翻译正确：普通、非普通、珍稀、极珍稀、传说、变体、神器

### 物品名称准确性 ✓
- 精金护甲 (Adamantine Armor) ✓
- 次元袋 (Bag of Holding) ✓
- 治疗药水 (Potion of Healing) ✓
- 防护戒指 (Ring of Protection) ✓
- 万法之牌 (Deck of Many Things) ✓
- 魔法飞弹魔杖 (Wand of Magic Missiles) ✓

### 格式规范性
- 所有物品都遵循 `name` + `name_en` 格式 ✓
- 所有物品都遵循 `desc` + `desc_en` 格式 ✓
- 部分物品描述第一行存在英文未翻译或翻译不完整的问题

### 完整性 ✓
- 所有 362 个物品都已翻译

## 问题列表

### 1. [格式错误] Belt of Dwarvenkind → 矮人腰带
- **位置：** desc[0]
- **问题描述：** 描述第一行包含英文 'Wondrous Items'，未翻译为 '奇物'
- **当前内容：** Wondrous Items, rare (需要调谐)
- **建议修正：** 将 'Wondrous Items, rare (需要调谐)' 改为 '奇物, 珍稀 (需要调谐)'

### 2. [拼写错误] Bracers of Defense → 防御护腕
- **位置：** desc[0]
- **问题描述：** 'Wondous' 拼写错误，且未翻译为中文
- **当前内容：** Wondous item, rare (需要调谐)
- **建议修正：** 将 'Wondous item, rare (需要调谐)' 改为 '奇物, 珍稀 (需要调谐)'

### 3. [翻译错误] Cloak of Elvenkind → 精灵斗篷
- **位置：** desc[1]
- **问题描述：** '兽皮甲' 翻译错误，原文是 'hide'（隐藏），不是 'hide armor'（兽皮甲）
- **当前内容：** While you wear this cloak with its hood up, 感知 (Perception) checks made to see y...
- **建议修正：** 将 '兽皮甲' 改为 '隐藏'

### 4. [翻译错误] Gold Dragon Scale Mail → 金龙鳞甲
- **位置：** desc[1]
- **问题描述：** '金币 dragon' 翻译错误，应为 '金龙'
- **当前内容：** Dragon scale mail is made of the scales of a 金币 dragon. Sometimes dragons collec...
- **建议修正：** 将 '金币 dragon' 改为 '金龙'

### 5. [翻译错误] Gold Dragon Scale Mail → 金龙鳞甲
- **位置：** desc[3]
- **问题描述：** '金币 dragon' 翻译错误，应为 '金龙'
- **当前内容：** Additionally, you can focus your senses as an 动作 to magically discern the distan...
- **建议修正：** 将 '金币 dragon' 改为 '金龙'

## 修正建议汇总

| 序号 | 物品索引 | 问题类型 | 修正内容 |
|-----|---------|---------|---------|
| 1 | belt-of-dwarvenkind | 格式错误 | 将 'Wondrous Items, rare (需要调谐)' 改为 '奇物, 珍稀 (需要调谐)'... |
| 2 | bracers-of-defense | 拼写错误 | 将 'Wondous item, rare (需要调谐)' 改为 '奇物, 珍稀 (需要调谐)'... |
| 3 | cloak-of-elvenkind | 翻译错误 | 将 '兽皮甲' 改为 '隐藏'... |
| 4 | dragon-scale-mail-gold | 翻译错误 | 将 '金币 dragon' 改为 '金龙'... |
| 5 | dragon-scale-mail-gold | 翻译错误 | 将 '金币 dragon' 改为 '金龙'... |

## 附录：关键术语对照表

### 装备分类
| 英文 | 标准中文 |
|-----|---------|
| Wondrous Items | 奇物 |
| Potion | 药水 |
| Ring | 戒指 |
| Weapon | 武器 |
| Armor | 护甲 |
| Wand | 魔杖 |
| Staff | 法杖 |
| Scroll | 卷轴 |
| Rod | 权杖 |
| Ammunition | 弹药 |

### 稀有度
| 英文 | 标准中文 |
|-----|---------|
| Common | 普通 |
| Uncommon | 非普通 |
| Rare | 珍稀 |
| Very Rare | 极珍稀 |
| Legendary | 传说 |
| Varies | 变体 |
| Artifact | 神器 |

---
*报告由自动化审查工具生成*
