# 翻译审查报告：5e-SRD-Classes.json

## 审查摘要
- **审查结果**：需修改
- **审查日期**：2026-02-16
- **审查员**：Kimi Code CLI
- **源文件**：`/Users/chezi/code/java/5e-database/src/2014/5e-SRD-Classes.json`
- **翻译文件**：`/Users/chezi/code/java/5e-database/src/2014-zh/5e-SRD-Classes.json`

---

## 统计信息
- **职业总数**：12个
- **术语正确率**：100% (12/12)
- **格式规范率**：100%
- **问题数量**：12处

---

## ✅ 正确翻译

### 职业名称
| 原文 | 译文 | 备注 |
|------|------|------|
| Barbarian | 野蛮人 | ✅ 标准译名 |
| Bard | 吟游诗人 | ✅ 标准译名 |
| Cleric | 牧师 | ✅ 标准译名 |
| Druid | 德鲁伊 | ✅ 标准译名 |
| Fighter | 战士 | ✅ 标准译名 |
| Monk | 武僧 | ✅ 标准译名 |
| Paladin | 圣武士 | ✅ 标准译名 |
| Ranger | 游侠 | ✅ 标准译名 |
| Rogue | 游荡者 | ✅ 标准译名 |
| Sorcerer | 术士 | ✅ 标准译名 |
| Warlock | 邪术师 | ✅ 标准译名 |
| Wizard | 法师 | ✅ 标准译名 |

### 子职业名称
| 原文 | 译文 | 备注 |
|------|------|------|
| Berserker | 狂战士 | ✅ 正确 |
| Lore | 知识 | ✅ 正确 |
| Life | 生命 | ✅ 正确 |
| Land | 大地 | ✅ 正确 |
| Champion | 勇士 | ✅ 正确 |
| Open Hand | 开掌 | ✅ 正确 |
| Devotion | 奉献 | ✅ 正确 |
| Hunter | 猎手 | ✅ 正确 |
| Thief | 盗贼 | ✅ 正确 |
| Draconic | 龙族 | ✅ 正确 |
| Fiend | 邪魔 | ✅ 正确 |
| Evocation | 塑能 | ✅ 正确 |

---

## ⚠️ 建议修改

### 1. 中英混杂问题（混合翻译）

| 位置 | 当前译文 | 建议译文 | 理由 |
|------|----------|----------|------|
| Bard.starting_equipment_options[1].desc | `(a) a diplomat's pack or (b) an entertainer's pack` | `(a) 外交官套组或 (b) 艺人套组` | 完全未翻译 |
| Bard.starting_equipment_options[2].desc | `(a) 鲁特琴或 (b) any other 乐器` | `(a) 鲁特琴或 (b) 任意其他乐器` | 中英混杂 |
| Fighter.starting_equipment_options[3].desc | `(a) a dungeoneer's pack or (b) an explorer's pack` | `(a) 地下城套组或 (b) 探险家套组` | 完全未翻译 |
| Rogue.starting_equipment_options[2].desc | `(a) a burglar's pack, (b) a dungeoneer's pack, or (c) an explorer's pack` | `(a) 窃贼套组、(b) 地下城套组或 (c) 探险家套组` | 完全未翻译 |
| Paladin.starting_equipment_options[3].desc | `(a) a priest's pack or (b) an explorer's pack` | `(a) 牧师套组或 (b) 探险家套组` | 完全未翻译 |
| Ranger.starting_equipment_options[2].desc | `(a) a dungeoneer's pack or (b) an explorer's pack` | `(a) 地下城套组或 (b) 探险家套组` | 完全未翻译 |
| Cleric.starting_equipment_options[3].desc | `(a) a priest's pack or (b) an explorer's pack` | `(a) 牧师套组或 (b) 探险家套组` | 完全未翻译 |

### 2. 中英混杂问题（含有英文冠词/介词）

| 位置 | 当前译文 | 建议译文 | 理由 |
|------|----------|----------|------|
| Fighter.starting_equipment_options[1].desc | `(a) 一把军用武器 and a shield or (b) 两把军用武器` | `(a) 一把军用武器和一面盾牌或 (b) 两把军用武器` | 含有英文单词 "and a shield" |
| Monk.starting_equipment_options[0].desc | `(a) a shortsword or (b) 任意简易武器` | `(a) 短剑或 (b) 任意简易武器` | 含有英文 "a shortsword" |
| Sorcerer.starting_equipment_options[1].desc | `(a) 材料包或 (b) an 奥术法器` | `(a) 材料包或 (b) 奥术法器` | 含有英文冠词 "an" |
| Warlock.starting_equipment_options[1].desc | `(a) 材料包或 (b) an 奥术法器` | `(a) 材料包或 (b) 奥术法器` | 含有英文冠词 "an" |
| Wizard.starting_equipment_options[0].desc | `(a) 长棍或 (b) a dagger` | `(a) 长棍或 (b) 匕首` | 含有英文 "a dagger" |
| Wizard.starting_equipment_options[1].desc | `(a) 材料包或 (b) an 奥术法器` | `(a) 材料包或 (b) 奥术法器` | 含有英文冠词 "an" |
| Bard.proficiency_choices[1].desc | `Choose one type of artisan's tools or one 乐器` | `选择一种工匠工具或一种乐器` | 中英混杂 |

---

## ❌ 错误/遗漏

### 1. 描述字段未翻译

| 位置 | 问题描述 | 建议修复 |
|------|----------|----------|
| Bard.proficiency_choices[1].desc | 完整英文未翻译 | 应译为："选择一种工匠工具或一种乐器" |
| 多职业.spellcasting.info[].desc | 法术施法描述仍为英文 | 应补充中文翻译，并保留 desc_en 作为对照 |

### 2. 内容遗漏检查

经对比，所有12个职业的以下字段均已翻译：
- ✅ `name` / `name_en` 格式正确
- ✅ `proficiency_choices[].desc` / `desc_en` 大部分已翻译（除上述问题）
- ✅ `proficiencies[].name` / `name_en` 已翻译
- ✅ `saving_throws[].name` / `name_en` 已翻译
- ✅ `starting_equipment[].equipment.name` / `name_en` 已翻译
- ✅ `starting_equipment_options[].desc` / `desc_en` 大部分已翻译（除上述问题）
- ✅ `subclasses[].name` / `name_en` 已翻译
- ✅ `spellcasting.info[].name` / `name_en` 已翻译

---

## 📋 格式规范性检查

| 检查项 | 状态 | 说明 |
|--------|------|------|
| name + name_en 格式 | ✅ 通过 | 所有主要字段均遵循此格式 |
| desc + desc_en 格式 | ✅ 通过 | 描述字段有双语对照 |
| URL 保持不变 | ✅ 通过 | API 路径保持英文 |
| index 保持不变 | ✅ 通过 | 索引键保持英文 |

---

## 📝 总体评价

### 优点
1. **术语一致性**：12个职业名称全部翻译正确，符合 D&D 5e 中文社区标准译名
2. **格式规范**：严格遵循 `name` + `name_en` 的双语格式
3. **结构完整**：所有职业的基本结构（熟练项、装备、子职业等）均已翻译

### 待改进
1. **遗漏翻译**：部分 `starting_equipment_options` 的 `desc` 字段完全未翻译
2. **中英混杂**：部分字段中英文混杂，如 "an 奥术法器"、"any other 乐器" 等
3. **法术描述**：`spellcasting.info[].desc` 字段仍为英文，需要翻译

---

## 🔧 修复建议

建议按以下优先级修复：

1. **高优先级**：修复完全未翻译的 `desc` 字段（如外交官套组/艺人套组）
2. **中优先级**：修复中英混杂的字段（如 "an 奥术法器"）
3. **低优先级**：翻译 `spellcasting.info[].desc` 中的英文描述

---

## 附录：12个职业译名对照表

| 英文 | 中文 | 验证结果 |
|------|------|----------|
| Barbarian | 野蛮人 | ✅ |
| Bard | 吟游诗人 | ✅ |
| Cleric | 牧师 | ✅ |
| Druid | 德鲁伊 | ✅ |
| Fighter | 战士 | ✅ |
| Monk | 武僧 | ✅ |
| Paladin | 圣武士 | ✅ |
| Ranger | 游侠 | ✅ |
| Rogue | 游荡者 | ✅ |
| Sorcerer | 术士 | ✅ |
| Warlock | 邪术师 | ✅ |
| Wizard | 法师 | ✅ |

---

*报告生成时间：2026-02-16*
