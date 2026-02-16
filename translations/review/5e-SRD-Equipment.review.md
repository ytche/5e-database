# 5e-SRD-Equipment 翻译审查报告

## 审查统计
- 审查时间：2026-02-16
- 审查装备总数：237
- 问题数量：12

## 总体评价
翻译质量良好，所有关键装备名称、武器属性、护甲分类、伤害类型等术语均符合 GLOSSARY.md 规范。

## 问题列表

### 1. [术语缺失] gear_category.name 未翻译
- 位置：以下 12 个装备
- 问题描述：gear_category.name 字段仍保留英文，应翻译为中文
- 建议修正：

| 装备 index | 当前值 | 建议值 |
|-----------|--------|--------|
| amulet | Holy Symbols | 圣徽 |
| emblem | Holy Symbols | 圣徽 |
| reliquary | Holy Symbols | 圣徽 |
| crystal | Arcane Foci | 奥术法器 |
| orb | Arcane Foci | 奥术法器 |
| rod | Arcane Foci | 奥术法器 |
| staff | Arcane Foci | 奥术法器 |
| wand | Arcane Foci | 奥术法器 |
| sprig-of-mistletoe | Druidic Foci | 德鲁伊法器 |
| totem | Druidic Foci | 德鲁伊法器 |
| wooden-staff | Druidic Foci | 德鲁伊法器 |
| yew-wand | Druidic Foci | 德鲁伊法器 |

## 修正建议汇总（JSON Patch 格式）

```json
[
  {
    "path": "amulet.gear_category.name",
    "current": "Holy Symbols",
    "suggested": "圣徽"
  },
  {
    "path": "emblem.gear_category.name",
    "current": "Holy Symbols",
    "suggested": "圣徽"
  },
  {
    "path": "reliquary.gear_category.name",
    "current": "Holy Symbols",
    "suggested": "圣徽"
  },
  {
    "path": "crystal.gear_category.name",
    "current": "Arcane Foci",
    "suggested": "奥术法器"
  },
  {
    "path": "orb.gear_category.name",
    "current": "Arcane Foci",
    "suggested": "奥术法器"
  },
  {
    "path": "rod.gear_category.name",
    "current": "Arcane Foci",
    "suggested": "奥术法器"
  },
  {
    "path": "staff.gear_category.name",
    "current": "Arcane Foci",
    "suggested": "奥术法器"
  },
  {
    "path": "wand.gear_category.name",
    "current": "Arcane Foci",
    "suggested": "奥术法器"
  },
  {
    "path": "sprig-of-mistletoe.gear_category.name",
    "current": "Druidic Foci",
    "suggested": "德鲁伊法器"
  },
  {
    "path": "totem.gear_category.name",
    "current": "Druidic Foci",
    "suggested": "德鲁伊法器"
  },
  {
    "path": "wooden-staff.gear_category.name",
    "current": "Druidic Foci",
    "suggested": "德鲁伊法器"
  },
  {
    "path": "yew-wand.gear_category.name",
    "current": "Druidic Foci",
    "suggested": "德鲁伊法器"
  }
]
```

## 术语一致性检查结果

### ✅ 武器属性（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| Light | 轻型 | ✓ |
| Finesse | 灵巧 | ✓ |
| Thrown | 投掷 | ✓ |
| Two-Handed | 双手 | ✓ |
| Versatile | 两用 | ✓ |
| Heavy | 重型 | ✓ |
| Reach | 触及 | ✓ |
| Loading | 装填 | ✓ |
| Special | 特殊 | ✓ |
| Ammunition | 弹药 | ✓ |
| Monk | 武僧 | ✓ |

### ✅ 武器分类（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| Simple | 简易 | ✓ |
| Martial | 军用 | ✓ |
| Melee | 近战 | ✓ |
| Ranged | 远程 | ✓ |

### ✅ 护甲分类（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| Light | 轻甲 | ✓ |
| Medium | 中甲 | ✓ |
| Heavy | 重甲 | ✓ |
| Shield | 盾牌 | ✓ |

### ✅ 伤害类型（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| Bludgeoning | 钝击 | ✓ |
| Piercing | 穿刺 | ✓ |
| Slashing | 挥砍 | ✓ |

### ✅ 易混淆装备名称（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| Club | 短棒 | ✓ |
| Greatclub | 巨棒 | ✓ |
| Spear | 矛 | ✓ |
| Pike | 长矛 | ✓ |
| Chain Shirt | 链甲衫 | ✓ |
| Chain Mail | 锁子甲 | ✓ |
| Light Hammer | 轻锤 | ✓ |
| Warhammer | 战锤 | ✓ |
| Maul | 巨锤 | ✓ |
| Bedroll | 铺盖 | ✓ |
| Waterskin | 水袋 | ✓ |

### ✅ 货币单位（全部正确）
| 英文 | 中文 | 状态 |
|-----|------|------|
| gp | 金币 | ✓ |
| sp | 银币 | ✓ |
| cp | 铜币 | ✓ |

## 格式规范性检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| name + name_en 格式 | ✓ | 所有 237 个装备均符合 |
| index 未翻译 | ✓ | 所有 index 保持原样 |
| url 未翻译 | ✓ | 所有 url 保持原样 |
| desc + desc_en | ✓ | 所有描述字段均保留英文原文 |

## 完整性检查

| 检查项 | 数量 | 状态 |
|--------|------|------|
| 总装备数 | 237 | ✓ 与英文版一致 |
| 武器 | 37 | ✓ |
| 护甲 | 13 | ✓ |
| 冒险装备 | 116 | ✓ |
| 工具 | 31 | ✓ |
| 坐骑与载具 | 40 | ✓ |

## 术语表贡献

本次翻译中出现的新术语建议添加到 GLOSSARY.md：

| 英文 | 中文 | 类别 |
|------|------|------|
| Arcane Foci | 奥术法器 | 装备分类 |
| Druidic Foci | 德鲁伊法器 | 装备分类 |
| Holy Symbols | 圣徽 | 装备分类 |

---
*报告生成时间：2026-02-16*
